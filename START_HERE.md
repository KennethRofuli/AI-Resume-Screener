# 🎯 Quick Start - Run This!

## Option 1: Automated Start (Easiest)

### Windows (PowerShell - Recommended)
```powershell
.\start.ps1
```

### Windows (Command Prompt)
```cmd
start.bat
```

This will automatically start both the backend API and frontend React app!

## Option 2: Manual Start

### Step 1: Start Backend API
Open Terminal 1:
```bash
# Activate virtual environment
.venv\Scripts\activate

# Start API (runs on http://localhost:8000)
python api.py
```

### Step 2: Start Frontend
Open Terminal 2:
```bash
# Go to frontend folder
cd frontend

# Start React app (runs on http://localhost:3000)
npm start
```

## 🎮 Using the App

1. Open browser to `http://localhost:3000`
2. Upload a resume (PDF, DOCX, or TXT)
3. Paste or type the job description
4. Click "Analyze Resume"
5. View detailed results!

## 🔧 First Time Setup

If this is your first time:

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install React dependencies
cd frontend
npm install
```

## 📱 Features

- ✅ Upload resume files
- ✅ Paste job descriptions
- ✅ AI-powered matching
- ✅ Skill analysis
- ✅ Score breakdown
- ✅ Recommendations
- ✅ Beautiful visualizations

## 🚀 Ready to Go!

Everything is set up! Just run the start script and enjoy! 🎉
