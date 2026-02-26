import os
import io
import json
from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pydantic import BaseModel
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY", "AIzaSyAine9-UvdEOkcZA3WEnyf8ueLY2dH_Zhg")
if api_key:
    genai.configure(api_key=api_key)

app = FastAPI(title="Doc-Extractor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Doc-Extractor API is running. Use /extract for POST requests.", "status": "online"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

class ExtractionResult(BaseModel):
    document_type: str
    extracted_data: Dict[str, Any]
    confidence_score: float

def extract_with_gemini(file_content: bytes, file_type: str) -> Dict[str, Any]:
    if not api_key:
        return {"error": "API Key not configured"}
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Simple prompt for structured extraction
    prompt = """
    ROLE: You are an expert Document Analysis and OCR specialist with 99.9% accuracy.
    TASK: Analyze the provided document and extract all identifying data into a precise JSON format.
    
    INSTRUCTIONS:
    1. Identify the EXACT document type (e.g., 'Property Sale Deed', 'Commercial Invoice', 'Passport', 'Medical Prescription').
    2. Extract all visible fields (Names, Dates, ID Numbers, Totals, Clauses, Addresses).
    3. If it's a legal document, capture parties involved, witnesses, and land survey numbers.
    4. If it's an invoice, capture line items, tax breakdown, and vendor details.
    
    OUTPUT FORMAT: Return ONLY a valid JSON object. No pre-amble. No markdown backticks.
    {
        "document_type": "string",
        "extracted_data": { 
            "field_name": "extracted_value" 
        },
        "confidence_score": float (0.0 to 1.0)
    }
    """
    
    try:
        # Gemini can handle PDF bytes directly in some versions, but we'll send it as part of the mult-modal prompt
        response = model.generate_content([
            prompt,
            {"mime_type": file_type, "data": file_content}
        ])
        
        # Clean the response text to get JSON
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
            
        return json.loads(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract", response_model=ExtractionResult)
async def extract_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and Images are supported.")
    
    content = await file.read()
    mime_type = file.content_type
    
    result = extract_with_gemini(content, mime_type)
    return result

@app.get("/health")
async def health_check():
    return {"status": "healthy", "api_key_configured": bool(api_key)}

if __name__ == "__main__":
    import uvicorn
    # The backend will run on 9000 internally or locally
    uvicorn.run(app, host="0.0.0.0", port=9000)
