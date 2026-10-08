# shap-lime-ddos-detection
Jaccard-based SHAP–LIME agreement analysis for XGBoost-based DDoS detection

Jaccard-Based SHAP--LIME Agreement Analysis for XGBoost-Based DDoS Detection
Project Overview
This project uses XGBoost to detect DDoS traffic from the
CIC-DDoS2019 dataset.
SHAP and LIME are used to explain the model predictions, and
Jaccard similarity is used to compare the important features
identified by both explainers.
The project also includes a web dashboard connected to a Flask
backend for displaying the detection and explainability results.
Objectives
- Develop an XGBoost-based DDoS detection model.
- Preprocess network-flow data from the CIC-DDoS2019 dataset.
- Generate model explanations using SHAP and LIME.
- Measure SHAP--LIME feature agreement using Jaccard similarity.
- Display the model and explainability results through an interactive
  dashboard.
Dataset
CIC-DDoS2019
The project uses the CIC-DDoS2019 dataset, which contains benign
traffic and multiple DDoS attack types with network-flow features.
Official dataset page:
https://www.unb.ca/cic/datasets/ddos-2019.html
Dataset Setup
The dataset is not included in this GitHub repository because of its
large size.
Step 1 --- Download the dataset
1. Open the official CIC-DDoS2019 dataset page:
   https://www.unb.ca/cic/datasets/ddos-2019.html
2. Go to the Download this dataset section at the bottom of the
   page.
3. Download the dataset files.
4. If the downloaded dataset is provided as a ZIP file, keep the ZIP
   file available locally.
Step 2 --- Create the dataset folder in VS Code
Inside your project folder, create:
XAI_CYBER/
└── dataset/
Step 3 --- Put the dataset in the folder
For this project, the backend expects the dataset archive at:
XAI_CYBER/dataset/CIC-DDoS2019.zip
So the final local structure should be:
XAI_CYBER/
│
├── dataset/
│   └── CIC-DDoS2019.zip
│
├── backend.py
├── final_dashboard.html
├── final_dashboard_connected.html
└── requirements.txt
Important: Keep the dataset/ folder on your computer. Do not
upload the dataset to GitHub.
Technologies / Tools
- Python
- XGBoost
- SHAP
- LIME
- Jaccard Similarity
- Pandas
- NumPy
- Scikit-learn
- Flask
- Flask-CORS
- HTML, CSS, JavaScript
- Visual Studio Code
- GitHub
How to Run the Project in VS Code
1. Save the complete project
Keep all project files in one folder:
XAI_CYBER/
Make sure the local dataset is placed in:
dataset/CIC-DDoS2019.zip
2. Open the project in VS Code
Open VS Code → File → Open Folder and select the XAI_CYBER folder.
Then open:
Terminal → New Terminal
Make sure the terminal is inside the XAI_CYBER folder.
3. Install the required packages
Run:
python -m pip install -r requirements.txt
4. Run the backend
Run:
python backend.py
Keep this terminal running while using the dashboard.
5. Open the dashboard
Open:
final_dashboard_connected.html
in your browser.
The connected dashboard communicates with the Flask backend.
How the System Works
CIC-DDoS2019 Dataset
        ↓
Data Preprocessing
        ↓
XGBoost DDoS Detection
        ↓
 ┌───────────┐
 │           │
SHAP        LIME
 │           │
 └─────┬─────┘
       ↓
Jaccard Similarity
       ↓
SHAP–LIME Agreement
       ↓
Dashboard Results
What the Dashboard Shows
The dashboard presents:
- DDoS detection/model results
- Model performance metrics
- SHAP important features
- LIME important features
- Jaccard similarity between SHAP and LIME
- SHAP--LIME agreement information
- Explainer recommendation based on the analysis
Results
The reported experimental results are:
  Metric        Result
  Accuracy      97.18%
  Precision     99.65%
  Recall        96.95%
  F1-Score      98.28%
  ROC-AUC       0.9947
SHAP--LIME Agreement
- Top features considered: 10
- Common features: 8
- Union of features: 12
- Jaccard similarity: 0.6667
- Agreement: 66.67%
For the aggregate analysis, the Jaccard value of 0.6667 is above the
predefined threshold of 0.50, resulting in LIME being selected.
For the examined locally disagreeing flow, the Jaccard similarity was
0.3333. The stability fallback reported 100% SHAP stability and
82.58% LIME stability, resulting in SHAP being selected for that
local case.
Project Files
XAI_CYBER/
│
├── dataset/
│   └── CIC-DDoS2019.zip        # Local only; not uploaded to GitHub
│
├── backend.py                  # Flask backend
├── final_dashboard.html        # Dashboard
├── final_dashboard_connected.html
│                                # Dashboard connected to backend
├── requirements.txt             # Python dependencies
└── README.md
Authors
Department of Computer Science (Data Science)
Anjuman-I-Islam's Kalsekar Technical Campus (AIKTC)
Panvel, Maharashtra, India
Project Team
- Alfiya Khan
- Saniya Koyal
- Ishrat Mansuri
- Nishta Mayekar
Research Paper
Jaccard-Based SHAP--LIME Agreement Analysis for XGBoost-Based DDoS
Detection
This repository contains the project implementation and supporting files
for the research work.
