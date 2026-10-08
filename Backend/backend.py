import os
import glob
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier
import shap
from lime.lime_tabular import LimeTabularExplainer

BASE = Path(__file__).resolve().parent
ZIP_PATH = BASE / "dataset" / "CIC-DDoS2019.zip"
EXTRACT_DIR = BASE / "dataset" / "CIC-DDoS2019"

app = Flask(__name__)
CORS(app)

model = None
X_train = None
X_test = None
y_train = None
y_test = None
shap_top10 = None
lime_top10 = None
metrics = {}


def load_pool(files):
    frames = []
    for f in files:
        d = pd.read_parquet(f)
        d["source_file"] = os.path.basename(f).replace(".parquet", "")
        frames.append(d)
    return pd.concat(frames, ignore_index=True)


def prepare_data():
    if not ZIP_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {ZIP_PATH}"
        )

    if not EXTRACT_DIR.exists():
        EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(ZIP_PATH, "r") as z:
            z.extractall(EXTRACT_DIR)

    train_files = sorted(glob.glob(
        str(EXTRACT_DIR / "**" / "*-training.parquet"), recursive=True
    ))
    test_files = sorted(glob.glob(
        str(EXTRACT_DIR / "**" / "*-testing.parquet"), recursive=True
    ))

    if not train_files or not test_files:
        raise RuntimeError("Training/testing parquet files were not found.")

    train = load_pool(train_files)
    test = load_pool(test_files)

    train["binary_label"] = np.where(
        train["Label"].astype(str) == "Benign", "Benign", "Attack"
    )
    test["binary_label"] = np.where(
        test["Label"].astype(str) == "Benign", "Benign", "Attack"
    )

    drop = ["Label", "source_file"]
    Xtr = train.drop(columns=drop + ["binary_label"])
    Xte = test.drop(columns=drop + ["binary_label"])

    ytr = (train["binary_label"] == "Attack").astype(int)
    yte = (test["binary_label"] == "Attack").astype(int)

    Xtr = Xtr.replace([np.inf, -np.inf], np.nan)
    Xte = Xte.replace([np.inf, -np.inf], np.nan)

    a = Xtr.notna().all(axis=1)
    b = Xte.notna().all(axis=1)
    Xtr, ytr = Xtr.loc[a], ytr.loc[a]
    Xte, yte = Xte.loc[b], yte.loc[b]

    constant = [c for c in Xtr.columns if Xtr[c].nunique() <= 1]
    Xtr = Xtr.drop(columns=constant)
    Xte = Xte.drop(columns=[c for c in constant if c in Xte.columns])
    Xte = Xte[Xtr.columns]

    return Xtr.reset_index(drop=True), Xte.reset_index(drop=True), \
        ytr.reset_index(drop=True), yte.reset_index(drop=True)


def train():
    global model, X_train, X_test, y_train, y_test
    global shap_top10, lime_top10, metrics

    print("Loading CIC-DDoS2019...")
    X_train, X_test, y_train, y_test = prepare_data()

    model = XGBClassifier(
        n_estimators=50,
        max_depth=2,
        learning_rate=0.03,
        subsample=0.5,
        colsample_bytree=0.5,
        min_child_weight=10,
        gamma=1,
        reg_alpha=1,
        reg_lambda=5,
        random_state=42,
        eval_metric="logloss",
        n_jobs=-1
    )
    print("Training XGBoost...")
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y_test, pred) * 100, 2),
        "precision": round(precision_score(y_test, pred, zero_division=0) * 100, 2),
        "recall": round(recall_score(y_test, pred, zero_division=0) * 100, 2),
        "f1": round(f1_score(y_test, pred, zero_division=0) * 100, 2),
        "roc_auc": round(roc_auc_score(y_test, prob) * 100, 2)
    }

    # SHAP: same top-10 logic as the original project.
    n = min(2000, len(X_test))
    xs = X_test.sample(n=n, random_state=42)
    explainer = shap.TreeExplainer(model)
    sv = explainer.shap_values(xs)
    if isinstance(sv, list):
        sv = sv[1]

    importance = pd.DataFrame({
        "Feature": xs.columns,
        "Importance": np.abs(sv).mean(axis=0)
    }).sort_values("Importance", ascending=False)
    shap_top10 = importance.head(10)

    # LIME: keep the original project logic, but use a smaller sample so
    # the local Flask server is practical to run.
    lime_exp = LimeTabularExplainer(
        X_train.values,
        feature_names=X_train.columns.tolist(),
        class_names=["Benign", "Attack"],
        mode="classification",
        discretize_continuous=False,
        random_state=42
    )

    lime_n = min(200, len(xs))
    all_values = []

    for i in range(lime_n):
        e = lime_exp.explain_instance(
            xs.iloc[i].values,
            model.predict_proba,
            num_features=len(X_train.columns)
        )
        vals = dict(e.as_list())
        all_values.append([abs(vals.get(c, 0)) for c in X_train.columns])

    li = np.mean(all_values, axis=0)
    lime_importance = pd.DataFrame({
        "Feature": X_train.columns,
        "Importance": li
    }).sort_values("Importance", ascending=False)
    lime_top10 = lime_importance.head(10)

    print("Backend ready.")


def recommendation():
    s = set(shap_top10["Feature"])
    l = set(lime_top10["Feature"])
    union = s | l
    j = len(s & l) / len(union) if union else 0

    if j >= 0.70:
        confidence, status, selected = "High", "AGREE", "LIME"
        reason = "High agreement between SHAP and LIME"
    elif j >= 0.50:
        confidence, status, selected = "Medium", "AGREE", "LIME"
        reason = "Moderate agreement between SHAP and LIME"
    else:
        confidence, status, selected = "Low", "DISAGREE", "SHAP"
        reason = "Low agreement - SHAP used as fallback"

    return {
        "status": "completed",
        "jaccard": round(j * 100, 2),
        "agreement": status,
        "confidence": confidence,
        "recommendation": selected,
        "reason": reason,
        "metrics": metrics
    }


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None
    })


@app.post("/api/analyze")
def analyze():
    if model is None:
        return jsonify({
            "status": "error",
            "message": "Model is not loaded."
        }), 500

    uploaded = request.files.get("dataset")

    try:
        result = recommendation()

        if uploaded and uploaded.filename:
            if not uploaded.filename.lower().endswith(".csv"):
                return jsonify({
                    "status": "error",
                    "message": "Only CSV files are supported."
                }), 400

            custom = pd.read_csv(uploaded)
            custom = custom.drop(
                columns=["Label", "binary_label", "source_file"],
                errors="ignore"
            )

            missing = [c for c in X_train.columns if c not in custom.columns]
            if missing:
                return jsonify({
                    "status": "error",
                    "message": (
                        "This CSV is not compatible with the trained "
                        "CIC-DDoS2019 feature set."
                    ),
                    "missing_columns": missing[:20]
                }), 400

            custom = custom[X_train.columns]
            custom = custom.replace([np.inf, -np.inf], np.nan).dropna()

            if custom.empty:
                return jsonify({
                    "status": "error",
                    "message": "No valid rows remain in the uploaded CSV."
                }), 400

            predictions = model.predict(custom)
            result["uploaded_file"] = uploaded.filename
            result["rows_analyzed"] = int(len(custom))
            result["predicted_attacks"] = int((predictions == 1).sum())
            result["predicted_benign"] = int((predictions == 0).sum())

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    train()
    print("XAI backend: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)