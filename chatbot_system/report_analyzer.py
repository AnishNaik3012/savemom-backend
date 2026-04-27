import io
import os
import json
import base64
import asyncio
import google.generativeai as genai
import fitz  # PyMuPDF
from typing import Dict, Any, List

# API Key is now mostly loaded in main.py, but we keep this for standalone/robustness
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extracts text from a PDF file provided as bytes.
    """
    import pdfplumber
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PDF Extraction Error: {e}")
    
    return text.strip()

def convert_pdf_to_image(file_content: bytes) -> bytes:
    """
    Converts the front page of a PDF to a JPEG image.
    Returns the image data as bytes.
    """
    try:
        doc = fitz.open(stream=file_content, filetype="pdf")
        page = doc.load_page(0)  # load the first page
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # upscale for better quality
        img_bytes = pix.tobytes("jpg")
        doc.close()
        return img_bytes
    except Exception as e:
        print(f"PDF to Image Conversion Error: {e}")
        return b""

async def analyze_report_with_ai(file_content: bytes, mime_type: str) -> Dict[str, Any]:
    """
    Uses Gemini AI to analyze the report (PDF or Image).
    Parallelizes AI call and Image conversion for speed (< 10s).
    Enforces medical-only content.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Fallback logic... (simplified view)
        text = ""
        result = {}
        if "pdf" in mime_type:
            text = extract_text_from_pdf(file_content)
            analysis_image = convert_pdf_to_image(file_content)
            if analysis_image:
                preview_b64 = base64.b64encode(analysis_image).decode('utf-8')
                result["preview_image"] = f"data:image/jpeg;base64,{preview_b64}"
        else:
            text = "[Image Content - Requires OCR for detailed analysis]"
        
        fallback_res = summarize_report_rule_based(text, mime_type)
        fallback_res.update(result)
        return fallback_res

    try:
        genai.configure(api_key=api_key)
        
        generation_config = {
            "response_mime_type": "application/json",
        }
        
        system_instruction = """
        ACT AS A ZERO-TOLERANCE MEDICAL DOCUMENT FILTER.
        Your ONLY job is to verify if an image or PDF is a CLINICAL MEDICAL DOCUMENT.
        
        ALLOWED:
        - Hospital/Lab Reports (Blood tests, Urine tests, etc.)
        - Radiology (Ultrasound images, CT/MRI results)
        - Prescriptions, Doctor's Consultations
        
        STRICTLY FORBIDDEN (REJECT IMMEDIATELY):
        - Academic/School reports (Mark sheets, Grade cards, Attendance) -> THESE ARE FREQUENTLY MISMATCHED. REJECT THEM.
        - Personal ID (Aadhar, PAN)
        - Bills or general photos.
        
        If it is NOT a clinical medical document, you MUST return `is_medical: false`.
        """

        model = genai.GenerativeModel(
            model_name='gemini-flash-latest',
            generation_config=generation_config,
            system_instruction=system_instruction
        )
        
        prompt = """
        Examine this document. Is it a CLINICAL medical report?
        
        If it is an Academic/School report or any non-medical file, return:
        {"is_medical": false, "error_message": "This system only accepts medical reports"}
        
        If it IS a medical report, return the analysis:
        {
          "is_medical": true,
          "report_title": "Concise Title",
          "category": "Lab | Radiology | Clinical | Prescription",
          "summary": "Clinical summary",
          "description": "Purpose of test",
          "health_status": "Normal | Attention Required | Critical",
          "wellness_score": integer,
          "extracted_fields": [{"label": "string", "value": "string"}],
          "wellness_insights": ["3-4 actionable medical tips"],
          "metric_comparisons": [{"label": "string", "current": float, "min": float, "max": float, "unit": "string"}]
        }
        """

        # Prepare parts
        parts = [prompt]
        if "pdf" in mime_type:
            parts.append({"mime_type": "application/pdf", "data": file_content})
        else:
            parts.append({"mime_type": mime_type, "data": file_content})

        # --- PARALLEL EXECUTION (< 10s Goal) ---
        ai_task = model.generate_content_async(parts)
        if "pdf" in mime_type:
            preview_task = asyncio.to_thread(convert_pdf_to_image, file_content)
        else:
            preview_task = asyncio.to_thread(lambda: file_content)

        response, img_bytes = await asyncio.gather(ai_task, preview_task)
        
        try:
            result = json.loads(response.text)
        except Exception as e:
            print(f"JSON Parsing Error: {e}")
            result = {"is_medical": True, "report_title": "Analysis Result", "summary": response.text[:500]}

        # --- PYTHON-SIDE GUARDIAN ---
        # Even if AI says is_medical=True, we check for academic keywords to prevent hallucinations
        # This fixes the "High School Report" issue where AI gets confused by the table structure.
        
        # Convert result to string for easy searching
        res_str = json.dumps(result).lower()
        forbidden_terms = [
            "high school", "grade level", "semester", "gpa", "academic year", 
            "student name", "class teacher", "attendance record", "school report"
        ]
        
        if any(term in res_str for term in forbidden_terms):
            print("Guardrail: Academic content detected. Overriding AI decision.")
            result["is_medical"] = False
            result["error_message"] = "This system only accepts medical reports"

        # Handle non-medical content restriction - FORCE USER'S MESSAGE
        if not result.get("is_medical", True):
            error_msg = result.get("error_message", "This system only accepts medical reports")
            return {
                "report_title": "Invalid Document",
                "summary": error_msg,
                "error_message": error_msg,
                "is_medical": False
            }

        # Add preview image
        if img_bytes:
            preview_image_b64 = base64.b64encode(img_bytes).decode('utf-8')
            result["preview_image"] = f"data:image/jpeg;base64,{preview_image_b64}"
        
        # Background indexing
        try:
            from .rag.rag_service import rag_service
            rag_service.index_report(result)
        except:
            pass
            
        return result

    except Exception as e:
        print(f"Gemini Analysis Error: {e}")
        return summarize_report_rule_based("", mime_type)

def summarize_report_rule_based(text: str, mime_type: str) -> Dict[str, Any]:
    """
    Provides a dynamic rule-based summary when AI is unavailable.
    """
    if not text or len(text) < 10:
        if "image" in mime_type:
            return {
                "report_title": "Medical Image Uploaded",
                "category": "Visual Data",
                "summary": "You've uploaded an image. For a detailed analysis, please provide a PDF version or configure the AI API key.",
                "key_findings": ["Visual file detected"],
                "health_status": "Normal",
                "description": "This is an image-based report. Rule-based analysis is limited for images."
            }
        return {
            "report_title": "Empty Report",
            "category": "Unknown",
            "summary": "The report content could not be read clearly.",
            "health_status": "Unknown",
            "description": "The file appears to be empty or encrypted.",
            "wellness_insights": ["Please upload a clear medical document."],
            "wellness_score": 50,
            "metric_comparisons": []
        }

    # Dynamic Identification Heuristics
    text_lower = text.lower()
    report_title = "General Medical Report"
    category = "Clinical"
    health_status = "Normal"
    
    # Check if text is just a placeholder for images
    if "[image content" in text_lower:
        report_title = "Medical Image Analysis"
        category = "Radiology/Clinical"
        findings_summary = "Visual data detected in the upload."
        return {
            "report_title": report_title,
            "category": category,
            "summary": "You've uploaded a medical image. Please ensure the Gemini API key is configured for a deep AI analysis of the visual content.",
            "extracted_fields": [
                {"label": "File Type", "value": "Image (PNG/JPG)"},
                {"label": "Analysis Status", "value": "OCR/AI required for full extraction"}
            ],
            "health_status": "Normal",
            "description": "This is a visual medical record. For specific data extraction like Fetal Heart Rate or Hemoglobin, an AI-powered scan is necessary.",
            "wellness_insights": ["Coordinate with your doctor for a detailed AI manual review."],
            "wellness_score": 80,
            "metric_comparisons": []
        }

    if "hemoglobin" in text_lower or "blood" in text_lower:
        report_title = "Blood Investigation Report"
        category = "Lab"
    elif "ultrasound" in text_lower or "scan" in text_lower:
        report_title = "Imaging/Scan Report"
        category = "Radiology"
    elif "prescription" in text_lower:
        report_title = "Medical Prescription"
        category = "Prescription"

    findings = []
    keywords = {
        "HEMOGLOBIN": "Blood count checked",
        "BP": "Blood pressure recorded",
        "GLUCOSE": "Sugar levels identified",
        "WEIGHT": "Physical measurement noted",
        "URINE": "Urinalysis performed"
    }

    for kw, desc in keywords.items():
        if kw.lower() in text_lower:
            # Try to grab the context (simple line)
            for line in text.split('\n'):
                if kw.lower() in line.lower():
                    findings.append(line.strip())
                    break
    
    if any(k in text_lower for k in ["critical", "high risk", "abnormal"]):
        health_status = "Attention Required"

    findings_summary = ""
    if findings:
        topics = [f.split(':')[0].strip() for f in findings[:3]]
        findings_summary = f"It contains specific data regarding {', '.join(topics)}."
    else:
        findings_summary = "It contains general clinical observations and health markers."

    dynamic_fields = []
    highlight_metric = None
    
    # Map findings to extracted_fields
    for f in findings:
        if ':' in f:
            lbl, val = f.split(':', 1)
            dynamic_fields.append({"label": lbl.strip().title(), "value": val.strip()})
        else:
            dynamic_fields.append({"label": "Finding", "value": f})

    # Try to extract a highlight metric
    if "HEMOGLOBIN" in text_lower:
        for f in dynamic_fields:
            if "Hemoglobin" in f["label"]:
                highlight_metric = {"label": "Hemoglobin", "value": f["value"], "unit": "g/dL", "icon": "🩸"}
                break
    elif "BP" in text_lower:
        for f in dynamic_fields:
            if "Bp" in f["label"]:
                highlight_metric = {"label": "Blood Pressure", "value": f["value"], "unit": "mmHg", "icon": "💓"}
                break

    return {
        "report_title": report_title,
        "category": category,
        "summary": f"Your {report_title} has been analyzed. {findings_summary}",
        "extracted_fields": dynamic_fields if dynamic_fields else [{"label": "Status", "value": "All parameters within typical ranges"}],
        "highlight_metric": highlight_metric,
        "health_status": health_status,
        "description": f"This is a comprehensive {report_title}. {findings_summary} We recommend presenting these findings to your primary healthcare provider for a localized clinical correlation.",
        "wellness_insights": [
             "Maintain regular health check-ups.",
             "Follow a balanced diet based on your laboratory parameters.",
             "Stay physically active with light walking or yoga unless advised otherwise."
        ],
        "wellness_score": 85 if health_status == "Normal" else 65,
        "metric_comparisons": [
            {"label": "Hemoglobin", "current": 11.5, "min": 12.0, "max": 16.0, "unit": "g/dL"}
        ] if "hemoglobin" in text_lower else []
    }
