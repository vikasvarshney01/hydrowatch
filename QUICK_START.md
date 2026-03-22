# 🚀 Quick Start Guide

## Current Status
✅ App is running at: http://localhost:8501
✅ Environment variables configured
✅ python-dotenv installed
⚠️ Firebase credentials needed (see below)

## To Enable Firebase Authentication

### Quick Steps:

1. **Download Firebase Credentials:**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create/select your project
   - Project Settings → Service Accounts → Generate New Private Key
   - Save as `firebase-credentials.json` in project root

2. **Place the file here:**
   ```
   /workspaces/HydroWatch-Water-Quality-Monitoring-and-Prediction-System/firebase-credentials.json
   ```

3. **Get Firebase API Key:**
   - Firebase Console → Project Settings → Web App
   - Copy the API Key (starts with `AIzaSy...`)
   - Replace in `components/account_page.py` (lines ~48 and ~77)

4. **Restart app:**
   ```bash
   pkill -f streamlit
   streamlit run app.py
   ```

## Detailed Instructions
See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for complete step-by-step guide.

## What Works Now:
✅ Home page
✅ Explore Database page
✅ Prediction Model (Guest Mode)
⚠️ Account page (needs Firebase credentials)
⚠️ Prediction Model (Registered Mode - needs Firebase)

## Files Created:
- `.env` - Environment variables (already configured)
- `FIREBASE_SETUP.md` - Detailed Firebase setup instructions
- `.gitignore` - Updated to protect sensitive files
