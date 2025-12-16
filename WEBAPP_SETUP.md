# 🚀 AI Resume Screener - Web App Setup

## Quick Start

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 2. Start the Backend API

Open a terminal and run:

```bash
# Activate virtual environment
.venv\Scripts\activate

# Start API server (runs on port 8000)
python api.py
```

You should see:
```
🚀 Starting AI Resume Screener API...
📖 API Documentation: http://localhost:8000/docs
```

### 3. Start the React Frontend

Open a **new terminal** and run:

```bash
cd frontend
npm start
```

The app will open at `http://localhost:3000`

## 🎯 Using the Web App

1. **Upload Resume**: Drag & drop or click to upload (PDF, DOCX, TXT)
2. **Job Description**: Paste the job posting text
3. **Analyze**: Click the analyze button
4. **View Results**: See detailed scoring, matched/missing skills, and recommendations

## 📁 Project Structure

```
AI Resume Checker/
├── frontend/                    # React web app
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── ResumeUpload.js
│   │   │   ├── JobInput.js
│   │   │   ├── AnalysisResults.js
│   │   │   ├── ScoreCard.js
│   │   │   ├── SkillsChart.js
│   │   │   └── LoadingSpinner.js
│   │   ├── services/
│   │   │   └── api.js          # API integration
│   │   ├── App.js              # Main component
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
├── resume_screener/            # Python backend
├── api.py                      # FastAPI server
└── requirements.txt
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in project root:

```env
# Backend
API_HOST=0.0.0.0
API_PORT=8000

# Frontend (optional)
REACT_APP_API_URL=http://localhost:8000
```

## ✨ Features

### Frontend Features
- 📤 **Drag & Drop Upload**: Easy resume upload
- 📝 **Flexible Job Input**: Paste text or URL (URL coming soon)
- 📊 **Beautiful Dashboard**: Visual results with charts
- 🎨 **Responsive Design**: Works on desktop, tablet, mobile
- ⚡ **Real-time Analysis**: Fast processing with loading states
- 🎯 **Score Breakdown**: Detailed component scores
- 💡 **Actionable Insights**: Recommendations and improvements

### Backend API
- 🔌 **RESTful API**: Clean endpoint design
- 📄 **Multi-format Support**: PDF, DOCX, TXT parsing
- 🧠 **NLP Processing**: BERT/SBERT embeddings
- 🛡️ **Bias Detection**: Fair screening analysis
- 📊 **Batch Processing**: Multiple resume analysis

## 🌐 API Endpoints

```
POST /api/analyze-file          # Analyze resume file
POST /api/analyze               # Analyze text-based resume
POST /api/bias-check            # Check for bias
POST /api/batch-analyze         # Batch processing
GET  /api/skills                # Get skill database
GET  /docs                      # API documentation
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in frontend/package.json
"start": "PORT=3001 react-scripts start"
```

### API Connection Issues
- Ensure backend is running on port 8000
- Check firewall settings
- Verify `.env` configuration

### Module Not Found
```bash
# Frontend
cd frontend
npm install

# Backend
pip install -r requirements.txt
```

## 🚀 Deployment

### Frontend (Netlify/Vercel)
```bash
cd frontend
npm run build
# Deploy the 'build' folder
```

### Backend (Heroku/Railway)
```bash
# Procfile
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

## 📱 Screenshots

The web app features:
- Modern gradient design
- Card-based layout
- Interactive visualizations
- Smooth animations
- Mobile-responsive interface

## 🎉 Next Steps

1. ✅ Test with your own resumes
2. ✅ Customize scoring weights
3. ✅ Add URL scraping (future feature)
4. ✅ Implement batch upload UI
5. ✅ Add export to PDF/JSON
6. ✅ User authentication
7. ✅ Analytics dashboard

Enjoy your AI Resume Screener! 🎯
