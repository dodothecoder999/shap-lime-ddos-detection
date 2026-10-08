# Jaccard-Based SHAP–LIME Agreement Analysis for XGBoost-Based DDoS Detection

An explainable machine learning project for DDoS attack detection using **XGBoost**, with **SHAP** and **LIME** used to interpret model predictions and **Jaccard similarity** used to measure agreement between the two explainers.

## Overview

This project evaluates an XGBoost-based binary DDoS detector trained on the **CIC-DDoS2019** dataset. The system compares SHAP and LIME feature explanations and applies a threshold-based selection procedure to identify the preferred explainer for the analysis.

## Objectives

- Build an XGBoost-based binary DDoS detection model.
- Evaluate model performance on the CIC-DDoS2019 dataset.
- Generate feature explanations using SHAP and LIME.
- Measure SHAP–LIME agreement using Jaccard similarity.
- Present model and explainability results through a web dashboard.

## Results

| Metric | Result |
|---|---:|
| Accuracy | **97.18%** |
| Precision | **99.65%** |
| Recall | **96.95%** |
| F1-Score | **98.28%** |
| ROC-AUC | **0.9947** |
| Jaccard Agreement | **0.6667** |

The analysis used the same **2,000 sampled test flows** for SHAP and LIME. The aggregate top-feature comparison produced a Jaccard similarity of **0.6667**.

## Technologies

- Python
- XGBoost
- SHAP
- LIME
- Pandas
- NumPy
- Scikit-learn
- Flask
- Flask-CORS
- HTML / CSS / JavaScript

## Dataset

**CIC-DDoS2019**  
Canadian Institute for Cybersecurity, University of New Brunswick.

Official dataset page:  
https://www.unb.ca/cic/datasets/ddos-2019.html

The dataset is **not included in this repository** because of its size.

### Local Dataset Setup

Place the downloaded dataset ZIP file at:

```text
XAI_CYBER/
└── dataset/
    └── CIC-DDoS2019.zip
```

Keep the dataset only on your local machine.

## Project Structure

```text
shap-lime-ddos-detection/
│
├── frontend/
│   ├── final_dashboard.html
│   └── final_dashboard_connected.html
│
├── backend/
│   └── backend.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

> The dataset is kept locally and is not uploaded to GitHub.

## Run Locally in VS Code

### 1. Open the project

Open the project folder in VS Code.

### 2. Install dependencies

Open the VS Code terminal and run:

```bash
python -m pip install -r requirements.txt
```

### 3. Start the backend

Run:

```bash
python backend.py
```

Keep the terminal running while using the dashboard.

### 4. Open the dashboard

Open:

```text
final_dashboard_connected.html
```

in your browser.

The connected dashboard communicates with the Flask backend to display the analysis results.

## Dashboard

The dashboard presents:

- Model performance metrics
- Important SHAP features
- Important LIME features
- Jaccard similarity
- SHAP–LIME agreement
- Explainer recommendation

## Authors

**Alfiya Khan**  
**Saniya Koyal**  
**Ishrat Mansuri**  
**Nishta Mayekar**

Department of Computer Science (Data Science)  
Anjuman-I-Islam's Kalsekar Technical Campus (AIKTC), Panvel, Maharashtra, India

## Research

This repository accompanies the research paper:

**“Jaccard-Based SHAP–LIME Agreement Analysis for XGBoost-Based DDoS Detection”**

## Notes

- Do not upload the CIC-DDoS2019 dataset to this repository.
- Do not upload virtual environments, cache files, or other large generated files.
- Make sure the Flask backend is running before opening the connected dashboard.
