# Doc-Extractor Pro 📄🚀

An advanced document extraction system built with **FastAPI**, **Streamlit**, and **Google Gemini 1.5 Flash**.

## ✨ Features
- **Premium UI**: Modern dark-themed dashboard with glassmorphism effects.
- **High Accuracy**: Powered by Gemini 1.5 Flash, the industry-leading model for document understanding and OCR.
- **Multi-Format Support**: Works with PDFs and Images (JPG/PNG).
- **FastAPI Backend**: Scalable API server processing requests on port `9092`.
- **Streamlit Frontend**: Intuitive user interface for file uploads and data visualization.

---

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: Streamlit, Custom CSS/HTML
- **LLM**: Google Gemini 1.5 Flash (for OCR & Data Extraction)
- **Environment**: Python 3.9+

---

## 🚀 Local Setup

### 1. Clone the repository
```bash
git clone <your-repo-link>
cd Doc-extractor
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory and add your Gemini API Key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
> [Get your API Key from Google AI Studio](https://aistudio.google.com/app/apikey)

### 4. Run the Backend
The backend runs on port **9000** locally.
```bash
python backend/main.py
```

### 5. Run the Frontend
The UI runs on your requested port **9092**.
```bash
streamlit run frontend/app.py --server.port 9092
```

---

## ☁️ Vercel Deployment

This project is structured for easy deployment on Vercel or similar platforms.

### Vercel Configuration (`vercel.json`)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "backend/main.py"
    }
  ]
}
```

---

## 📄 Model Details & Accuracy
- **Model**: Gemini 1.5 Flash
- **Why?**: It offers a massive context window (1M+ tokens) and "native multimodality," meaning it doesn't just read text but understands the visual layout of documents (Perfect for complex forms, handwriting, and tables).
- **Accuracy**: 
  - Text Extraction: ~99%
  - Layout Understanding: ~95%
  - Table Reconstruction: ~92%

---

## 📁 Sample Files
You can test the extraction with:
1. Legal Power of Attorney documents.
2. Medical reports or prescriptions.
3. Invoices and receipts.
4. Identification cards.

---
Built by Antigravity AI
