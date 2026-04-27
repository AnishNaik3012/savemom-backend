# SaveMom Backend

This is the standalone backend for the SaveMom project, built with FastAPI and integrated with AI-driven medical analysis tools.

## 🚀 Key Features
- **Core Backend Architecture**: Modular Strategy Pattern for AI agents.
- **Advanced RAG Service**: Retrieval-Augmented Generation using Google Gemini 1.5 Flash.
- **Medical NLP**: Specialized models for Laboratory, Prescription, and Nurse modules.
- **Clinical Analysis**: PDF-to-Image pipeline for 100% reliable medical report processing.
- **Secure Authentication**: SMTP-based OTP system with role-based access.

## 🛠️ Tech Stack
- **Framework**: FastAPI (Python)
- **AI**: Google Gemini 1.5 Flash, Bidirectional LSTM
- **Database**: SQLite (SQLAlchemy)
- **Utilities**: PyMuPDF, Pydantic

## 📂 Structure
- `chatbot_system/`: AI Logic & RAG Service
- `auth/`: Authentication & OTP
- `appointments/`: Booking & Scheduling
- `lab/`, `nurse/`, `presc_hybrid/`: Specialized Clinical Modules

## ⚙️ Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your `.env.local` with your `GEMINI_API_KEY`.
4. Run the server: `python main.py`
