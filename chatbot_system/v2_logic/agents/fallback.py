def fallback_agent(message: str):
    return {
        "type": "text",
        "response": (
            "I can help with appointments, pregnancy care, reports, "
            "and prescriptions. Please tell me what you need."
        )
    }
