# 🔥 Firebase Authentication Setup Guide

This guide will help you enable user authentication for HydroWatch.

## Step-by-Step Instructions

### 1️⃣ Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** or **"Create a project"**
3. Enter project name: `HydroWatch`
4. Disable Google Analytics (optional)
5. Click **"Create project"**

### 2️⃣ Enable Email Authentication

1. In your Firebase project, click **"Authentication"** in the left sidebar
2. Click **"Get started"**
3. Go to **"Sign-in method"** tab
4. Click on **"Email/Password"**
5. Toggle **"Enable"**
6. Click **"Save"**

### 3️⃣ Generate Service Account Key

1. Click the **gear icon** ⚙️ next to "Project Overview"
2. Select **"Project settings"**
3. Go to **"Service accounts"** tab
4. Click **"Generate new private key"**
5. Click **"Generate key"** button
6. A JSON file will be downloaded (e.g., `hydrowatch-firebase-adminsdk-xxxxx.json`)

### 4️⃣ Add Credentials to Your Project

1. **Rename** the downloaded JSON file to `firebase-credentials.json`
2. **Move** it to your project root directory:
   ```
   /workspaces/HydroWatch-Water-Quality-Monitoring-and-Prediction-System/firebase-credentials.json
   ```

### 5️⃣ Get Your Firebase API Key

1. In Firebase Console, go to **Project Settings** (gear icon)
2. Scroll down to **"Your apps"** section
3. Click the **Web icon** (</>)
4. Register your app with a nickname: `HydroWatch Web`
5. Copy the **API Key** from the config object (looks like `AIzaSy...`)
6. Open `components/account_page.py`
7. Replace the API key in **TWO places**:
   - Line ~48: `params={"key": "YOUR_API_KEY_HERE"}`
   - Line ~77: `params={"key": "YOUR_API_KEY_HERE"}`

### 6️⃣ Configure Environment Variables

The `.env` file has already been created for you with default values:

```bash
# Firebase Configuration
FIREBASE_CREDENTIALS=./firebase-credentials.json

# Database Configuration (Optional - for MySQL)
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=water_quality
```

**Note:** The `.env` and `firebase-credentials.json` files are in `.gitignore` and won't be committed to Git.

### 7️⃣ Restart the Application

```bash
pkill -f streamlit
streamlit run app.py
```

### 8️⃣ Test Authentication

1. Open the app at `http://localhost:8505` (or whichever port is shown)
2. Click **"👤 Account"** in the sidebar
3. You should now see the Sign In / Sign Up form
4. Create a test account with your email and password
5. Sign in and test the **Registered Mode** in the Prediction Model

---

## 📋 Checklist

- [ ] Firebase project created
- [ ] Email/Password authentication enabled
- [ ] Service account key downloaded
- [ ] `firebase-credentials.json` file in project root
- [ ] Firebase Web API key copied and replaced in `account_page.py`
- [ ] `.env` file configured (already done)
- [ ] `python-dotenv` installed (already done)
- [ ] Application restarted
- [ ] Authentication tested

---

## 🚨 Troubleshooting

### Error: "Firebase initialization failed"
- Check that `firebase-credentials.json` exists in project root
- Verify the path in `.env` file is correct
- Make sure the JSON file is valid (not corrupted)

### Error: "Signup failed" or "Login failed"
- Verify you replaced the API key in `account_page.py`
- Check that Email/Password authentication is enabled in Firebase Console
- Make sure your internet connection is working

### Firebase credentials not found
- Ensure the `.env` file exists
- Check that `FIREBASE_CREDENTIALS=./firebase-credentials.json` is set correctly
- Verify `python-dotenv` is installed: `pip list | grep dotenv`

---

## 🔒 Security Notes

⚠️ **IMPORTANT:** 
- Never commit `firebase-credentials.json` to Git
- Never commit `.env` file to Git
- These files are already in `.gitignore`
- For production deployment, use environment variables or secure secret management

---

## 📦 MySQL Database Setup (Optional)

If you want to enable database storage for registered users:

1. Install MySQL on your system
2. Update the database credentials in `.env`:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_NAME=water_quality
   ```
3. Restart the application

The database tables will be created automatically when a user makes their first prediction.

---

## ✅ Success!

Once setup is complete, you'll have:
- ✅ User registration and login
- ✅ Personalized prediction history
- ✅ User account management
- ✅ Data persistence for registered users

Happy monitoring! 🌊💧
