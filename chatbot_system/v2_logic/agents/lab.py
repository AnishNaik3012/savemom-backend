try:
    from lab.nlp import nlp_service as lab_nlp
except ImportError:
    lab_nlp = None

def lab_agent(message: str, user_role: str):
    """
    Handles queries about laboratory tests and results.
    Provides options to view history, upload reports, and understand results.
    """
    msg = message.lower()
    
    # 0. Try Lab NLP for sub-intent
    sub_intent = "None"
    if lab_nlp:
        sub_intent, confidence = lab_nlp.predict_intent(message)
        print(f"DEBUG: Lab Agent Sub-Intent: {sub_intent} ({confidence:.2f})")
    
    # 1. Handle "View History" intent
    if sub_intent == "view_lab_results" or "history" in msg or "my results" in msg or "last test" in msg:
        # In a real implementation, we would call service.get_patient_lab_history here.
        # For now, we provide a proactive response.
        return {
            "type": "text",
            "response": "I can help you review your lab history. Would you like me to pull up your most recent blood test results or show you a trend of your hemoglobin levels over time?",
            "buttons": [
                {"label": "📊 Recent Results", "action": "show recent lab history"},
                {"label": "📈 Hemoglobin Trend", "action": "show hemoglobin trend"}
            ]
        }
    
    # 2. Handle "Explain/Understand" intent
    if sub_intent == "interpret_report" or "explain" in msg or "what is" in msg or "normal" in msg:
        return {
            "type": "text",
            "response": "Laboratory results can be complex. I can explain common markers like Hemoglobin (Hb), Blood Glucose, or Thyroid (TSH) levels. Which one are you interested in?",
            "buttons": [
                {"label": "🩸 Hemoglobin (Hb)", "action": "explain hemoglobin"},
                {"label": "🍬 Blood Glucose", "action": "explain glucose"},
                {"label": "🦋 Thyroid (TSH)", "action": "explain thyroid"}
            ]
        }

    # 3. Handle "Request/Book Test" intent
    if sub_intent == "request_lab_test":
        return {
            "type": "text",
            "response": "I can help you book a lab test. Would you like to schedule a routine blood checkup or a specific investigation?",
            "buttons": [
                {"label": "🗓️ Schedule Routine", "action": "schedule routine checkup"},
                {"label": "🔍 Search Tests", "action": "search lab tests"}
            ]
        }

    # 3. Default Lab Response
    return {
        "type": "buttons",
        "response": "Welcome to the Lab Assistant. How can I help you with your laboratory reports today?",
        "buttons": [
            {"label": "📋 View Lab History", "action": "show lab history"},
            {"label": "📤 Upload Lab Report", "action": "upload report"},
            {"label": "💡 Understand Results", "action": "explain lab results"}
        ]
    }
