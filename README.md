# 🌿 Leaf Disease Detection System

An AI-powered system for detecting and diagnosing plant leaf diseases using computer vision and the Groq API.

## 📋 Features

- ✅ Real-time leaf disease detection
- 🔍 Image validation (rejects non-leaf images)
- 🦠 Multi-disease classification (fungal, bacterial, viral, pest, nutrient deficiency)
- 📊 Severity assessment and confidence scoring
- 💊 Treatment recommendations
- 🌐 RESTful API backend
- 🎨 Modern Streamlit web interface

## 🏗️ Architecture

```
┌─────────────────┐      HTTP/REST      ┌──────────────────┐
│   Streamlit     │ ◄─────────────────► │   FastAPI        │
│   Frontend      │    (Port 8501)      │   Backend        │
│   (main.py)     │                     │   (app.py)       │
└─────────────────┘                     └──────────────────┘
                                                 │
                                                 │
                                                 ▼
                                        ┌──────────────────┐
                                        │ LeafDisease      │
                                        │ Detector         │
                                        │ (mai.py)         │
                                        └──────────────────┘
                                                 │
                                                 │
                                                 ▼
                                        ┌──────────────────┐
                                        │   Groq API       │
                                        │   (Llama Vision) │
                                        └──────────────────┘
```

## 📁 Project Structure

```
LEAF/
├── app.py                  # FastAPI backend server
├── main.py                 # Streamlit frontend application
├── mai.py                  # Disease detector core logic
├── utils.py                # Utility functions for image processing
├── .env                    # Environment variables (API keys, config)
├── requirements.txt        # Python dependencies
├── run_backend.py          # Backend startup script
├── run_frontend.py         # Frontend startup script
└── README.md              # This file
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for API calls)

### 2. Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /path/to/LEAF
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install fastapi uvicorn[standard] python-multipart python-dotenv groq streamlit requests pillow
   ```

### 3. Configuration

1. **Check the `.env` file** - The API key is already configured:
   ```
   GROQ_API_KEY=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
   MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct
   API_PORT=5500
   ```

2. **Verify all files are present:**
   - app.py
   - main.py
   - mai.py
   - utils.py
   - .env

## 🎯 Running the Application

### Option 1: Using Helper Scripts (Recommended)

**Terminal 1 - Start Backend:**
```bash
python run_backend.py
```

**Terminal 2 - Start Frontend:**
```bash
python run_frontend.py
```

### Option 2: Manual Start

**Terminal 1 - Start Backend:**
```bash
uvicorn app:app --host 0.0.0.0 --port 5500 --reload
```

**Terminal 2 - Start Frontend:**
```bash
streamlit run main.py
```

## 🌐 Accessing the Application

Once both servers are running:

- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:5500
- **API Documentation**: http://localhost:5500/docs
- **Health Check**: http://localhost:5500/health

## 📱 How to Use

1. Open the frontend at http://localhost:8501
2. Click "Browse files" to upload a leaf image
3. Click "🔍 Detect Disease" button
4. Wait for analysis results
5. View disease information, symptoms, and treatment recommendations

## 🔧 API Endpoints

### POST /disease-detection-file
Upload a leaf image for disease detection.

**Request:**
- Content-Type: multipart/form-data
- Body: file (image file)

**Response:**
```json
{
  "disease_detected": true,
  "disease_name": "Bacterial Leaf Spot",
  "disease_type": "bacterial",
  "severity": "moderate",
  "confidence": 87.5,
  "symptoms": ["Dark spots on leaves", "..."],
  "possible_causes": ["Bacterial infection", "..."],
  "treatment": ["Remove affected leaves", "..."],
  "analysis_timestamp": "2026-02-14T..."
}
```

### GET /
API information endpoint

### GET /health
Health check endpoint

## 🧪 Testing the API

You can test the API directly using curl:

```bash
curl -X POST "http://localhost:5500/disease-detection-file" \
  -F "file=@/path/to/leaf_image.jpg"
```

Or use the interactive API documentation at http://localhost:5500/docs

## 🐛 Troubleshooting

### Backend won't start
- Check if port 5500 is already in use
- Verify GROQ_API_KEY is set in .env file
- Check Python version (requires 3.8+)

### Frontend can't connect to backend
- Ensure backend is running on port 5500
- Check firewall settings
- Verify API_URL in main.py matches backend address

### Import errors
- Install all dependencies: `pip install -r requirements.txt`
- Ensure all files (app.py, mai.py, utils.py) are in the same directory

### API errors
- Check your internet connection
- Verify Groq API key is valid
- Check API rate limits

## 📝 Environment Variables

Create or modify `.env` file:

```bash
# Required
GROQ_API_KEY=your_api_key_here

# Optional (with defaults)
MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct
MODEL_TEMPERATURE=0.3
MAX_COMPLETION_TOKENS=1024
API_HOST=0.0.0.0
API_PORT=5500
LOG_LEVEL=INFO
```

## 🔐 Security Notes

- Never commit `.env` file to version control
- Keep your API keys secure
- For production, use environment-specific configurations
- Implement rate limiting for public deployments

## 📊 Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)

## 🎨 Features in Detail

### Image Validation
The system automatically detects and rejects:
- Human faces/bodies
- Animals
- Objects (phones, cars, etc.)
- Buildings
- Non-plant images

### Disease Detection
Identifies:
- Fungal diseases
- Bacterial infections
- Viral diseases
- Pest damage
- Nutrient deficiencies
- Healthy leaves

### Analysis Output
For each detection:
- Disease name and type
- Severity assessment (mild/moderate/severe)
- Confidence score (0-100%)
- Visible symptoms
- Possible causes
- Treatment recommendations
- Timestamp

## 🚀 Production Deployment

For production deployment:

1. **Update .env for production:**
   - Use production API keys
   - Set appropriate logging levels
   - Configure proper CORS origins

2. **Use production WSGI server:**
   ```bash
   gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5500
   ```

3. **Secure your deployment:**
   - Use HTTPS
   - Implement authentication
   - Add rate limiting
   - Configure proper CORS policies

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at /docs
3. Check logs for error messages
4. Verify all dependencies are installed

## 📄 License

[Add your license information here]

## 🙏 Acknowledgments

- Groq API for AI inference
- FastAPI for the backend framework
- Streamlit for the frontend framework
- Llama Vision model for image analysis
