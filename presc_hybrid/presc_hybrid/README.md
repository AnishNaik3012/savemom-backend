# Prescription Analysis Module (Hybrid RAG + Gemini)

This module provides a robust backend for analyzing medical prescriptions using Google Gemini (Vision/Multimodal) and a localized RAG system for medical context.

## Features
- **Prescription Extraction**: Extracts structured data (Doctor, Patient, Medications, Dosage) from Images and PDFs.
- **Hybrid RAG**: Uses both Semantic Search (Vector) and Keyword Search (BM25) to retrieve medical context.
- **Medical QA**: Answer questions about the prescription or general medical queries using the RAG knowledge base.
- **API Ready**: Includes a FastAPI app for easy integration into chatbots or web backends.

## Installation

1.  **Clone/Download** the repository.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Validated with Python 3.10+*

3.  **Setup Environment**:
    Create a `.env` file in the root directory:
    ```env
    GOOGLE_API_KEY=your_actual_api_key_here
    ```

## Usage

### CLI (Command Line)
Analyze an image:
```bash
python main.py --image path/to/prescription.jpg
```

Ask a question with context:
```bash
python main.py --image path/to/prescription.jpg --question "What are the side effects of these meds?"
```

### API (FastAPI)
Start the server:
```bash
python app.py
```
or 
```bash
uvicorn app:app --reload
```

**Endpoints**:
- `POST /analyze`: Upload a file to get JSON data.
- `POST /ask`: Ask a question (optionally provide context).

### Python Integration
```python
from src.analyzer import PrescriptionAnalyzer

analyzer = PrescriptionAnalyzer()
result = analyzer.analyze_prescription("script.jpg")
print(result.medications)
```

## Project Structure
- `src/analyzer.py`: Main logic class.
- `src/rag_engine.py`: Hybrid Retrieval implementation.
- `src/loader.py`: File processing utilities.
- `src/models.py`: Pydantic data models.
