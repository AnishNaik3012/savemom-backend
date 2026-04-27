def report_agent(message: str, user_role: str):
    """
    Handles queries about medical reports.
    Provides options to upload, view summary, and a placeholder for voice toggle.
    """
    msg = message.lower()
    
    if "get summary" in msg or "summary" in msg:
        return {
            "type": "text",
            "response": "To see a dynamic summary of your medical report, please use the '📤 Upload Report' button below. Once you upload a PDF or an image, I will immediately analyze it and show you the key findings, health status, and a detailed description right here."
        }
    
    if "confirm report upload" in msg:
        return {
            "type": "text",
            "response": "✅ Medical report has been successfully analyzed and added to your records. How else can I assist you?"
        }

    return {
        "type": "buttons",
        "response": "How can I help you with your medical reports today?",
        "buttons": [
            {"label": "📤 Upload Report", "action": "upload report"}
        ]
    }
