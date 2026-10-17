# HydroWatch DFD

## Level 0 Context Diagram

```mermaid
flowchart LR
    U[User / Guest] -->|Water quality parameters, navigation, login/signup| S((HydroWatch Web App))
    R[Registered User] -->|Water quality parameters, account actions, view history| S

    S -->|Prediction result: Safe / Unsafe| U
    S -->|Prediction result, account status, history, analytics| R

    S -->|Authentication requests| F[Firebase Authentication]
    F -->|Token / auth response| S

    S -->|Read training and cleaned data| C[CSV Datasets]
    C -->|Sample rows, EDA data| S

    S -->|Load model for inference| M[Random Forest Model (.pkl)]
    M -->|Predictions| S

    S -->|Store and retrieve prediction history| D[(Firestore or MySQL)]
    D -->|Historical records| S
```

## Level 1 DFD

```mermaid
flowchart LR
    U[User / Guest]
    R[Registered User]

    P1((1. Home Page))
    P2((2. Database Exploration))
    P3((3. Prediction Model))
    P4((4. Account Management))
    P5((5. Database Handling))

    D1[(waterQualityPrediction.csv)]
    D2[(output_file.csv)]
    D3[(Rf_model.pkl)]
    D4[(Firebase Auth / Firestore)]
    D5[(MySQL WaterQualityMonitoringSystem)]

    U -->|Open app, browse pages| P1
    R -->|Open app, browse pages| P1

    U -->|Select Explore Database| P2
    R -->|Select Explore Database| P2
    P2 -->|Read original and cleaned datasets| D1
    P2 -->|Read cleaned dataset| D2
    P2 -->|Charts, histograms, heatmaps, interactive view| U
    P2 -->|Charts, histograms, heatmaps, interactive view| R

    U -->|Enter 20 water quality values| P3
    R -->|Enter 20 water quality values| P3
    P3 -->|Load sample rows for autofill| D1
    P3 -->|Load trained classifier| D3
    P3 -->|Prediction request| P5
    P5 -->|Persist prediction history| D4
    P5 -->|Persist prediction history| D5
    P3 -->|Safe / Unsafe result| U
    P3 -->|Safe / Unsafe result| R

    U -->|Sign up / login / reset password| P4
    R -->|View account and personalized analysis| P4
    P4 -->|Authenticate and verify user| D4
    P4 -->|Read prediction history| P5
    P5 -->|Fetch history and trends| D4
    P5 -->|Fetch history and trends| D5
    P4 -->|Session state and personalized status| R

    P1 -->|Navigation only| U
    P1 -->|Navigation only| R
```

## Notes

- The app entry point is [app.py](app.py), which routes to the four pages in `components/`.
- Prediction mode uses the trained Random Forest model stored in [Rf_model.pkl](Rf_model.pkl).
- The exploration page reads [waterQualityPrediction.csv](waterQualityPrediction.csv) and [output_file.csv](output_file.csv).
- Registered predictions are written to Firestore when Firebase is configured, otherwise they fall back to MySQL through [components/database_creation.py](components/database_creation.py).
- Guest mode predicts without saving history.
