import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional

# Standard imports for SaveMom environment
try:
    from db import SessionLocal
    from model import RAGKnowledge
except ImportError:
    # Fallback for standalone tests or path issues
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from db import SessionLocal
    from model import RAGKnowledge

class RAGService:
    _knowledge_base: List[Dict[str, Any]] = []
    _initialized: bool = False

    def _ensure_initialized(self):
        """Loads data from the database if not already done."""
        if not self._initialized:
            self._load_from_db()
            self._initialized = True

    def _load_from_db(self):
        print("RAG: Loading knowledge base from database...")
        db = SessionLocal()
        try:
            records = db.query(RAGKnowledge).all()
            self._knowledge_base = []
            for r in records:
                self._knowledge_base.append({
                    "report_title": r.report_title,
                    "category": r.category,
                    "summary": r.summary,
                    "description": r.description,
                    "health_status": r.health_status,
                    "wellness_score": r.wellness_score,
                    "raw_data": r.raw_data
                })
            print(f"RAG: Successfully loaded {len(self._knowledge_base)} entries from persistent storage.")
        except Exception as e:
            print(f"RAG: Persistent storage load error: {e}")
            # Keep empty or existing _knowledge_base
        finally:
            db.close()

    def index_report(self, report_data: Dict[str, Any]):
        """Indexes a new report in memory and persists it to the database."""
        self._ensure_initialized()
        
        # 1. Update in-memory cache
        self._knowledge_base.append(report_data)
        
        # 2. Persist to SQLite
        db = SessionLocal()
        try:
            new_entry = RAGKnowledge(
                report_title=report_data.get("report_title"),
                category=report_data.get("category"),
                summary=report_data.get("summary"),
                description=report_data.get("description"),
                health_status=report_data.get("health_status"),
                wellness_score=report_data.get("wellness_score"),
                raw_data=report_data
            )
            db.add(new_entry)
            db.commit()
            print(f"RAG: Persisted new report '{report_data.get('report_title')}' to persistent storage.")
        except Exception as e:
            print(f"RAG: Error persisting to DB: {e}")
            db.rollback()
        finally:
            db.close()

    def retrieve_context(self, query: str, limit: int = 3) -> str:
        """
        Retrieves relevant context using an improved AND-based keyword matching.
        Ensures higher precision by requiring all non-trivial query words to be present.
        """
        self._ensure_initialized()
        
        # Extract meaningful words (length > 2)
        query_words = [w.lower() for w in query.split() if len(w) > 2]
        if not query_words:
            return ""

        results = []
        for item in self._knowledge_base:
            content_to_check = f"{item.get('report_title', '')} {item.get('summary', '')} {item.get('description', '')}".lower()
            
            # Logic: Must contain ALL words from the query (more precise than original OR match)
            if all(word in content_to_check for word in query_words):
                results.append(item)
        
        if not results:
            return ""

        context_blocks = []
        for res in results[:limit]:
            block = f"Report: {res.get('report_title')}\nSummary: {res.get('summary')}\nDetails: {res.get('description')}"
            context_blocks.append(block)
            
        return "\n\n---\n\n".join(context_blocks)

    @staticmethod
    async def generate_hybrid_response(query: str, context: Optional[str] = None) -> str:
        """Generates a response using Gemini 1.5 Flash (Upgraded)."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Configuration Error: API Key missing."

        genai.configure(api_key=api_key)
        # Upgraded to gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')

        if context:
            prompt = f"Using the clinical context below, answer accurately. CONTEXT: {context} USER QUESTION: {query}"
        else:
            prompt = f"User Question: {query}"

        try:
            response = await model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Service Error: {str(e)}"

    @staticmethod
    async def generate_wellness_insight(patient_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generates maternal wellness insights using Gemini 1.5 Flash."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"error": "Configuration Error: API Key missing."}

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = """
        You are a maternal health expert assistant for SaveMom.
        Generate a personalized health insight and a 'Wellness Score' (1-100) for a pregnant mother.
        Data: {data}
        Return a JSON object with:
        - "insight": A warm, encouraging, and medically sound piece of advice (max 2 sentences).
        - "score": An integer from 1-100 representing general wellness based on data provided.
        - "category": One word (e.g., 'Nutrition', 'Activity', 'Hydration').
        If no data is provided, assume a generic healthy profile but give a relevant tip.
        """.format(data=patient_data or "Generic healthy profile")

        try:
            response = await model.generate_content_async(prompt)
            text = response.text
            import json
            import re
            
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            
            return {
                "insight": text if len(text) < 100 else "Stay hydrated and take your prenatal vitamins daily.",
                "score": 85,
                "category": "General"
            }
        except Exception as e:
            return {"error": f"Service Error: {str(e)}", "score": 0}

rag_service = RAGService()

