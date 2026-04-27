def maternal_agent(message: str, role: str):
    return {
        "type": "text",
        "response": (
            "I can help with general pregnancy-related information. "
            "However, I cannot diagnose conditions. "
            "If symptoms persist, please consult your doctor."
        )
    }
