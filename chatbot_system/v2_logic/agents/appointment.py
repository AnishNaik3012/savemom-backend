def appointment_agent(message: str, role: str):
    if role not in ["parent", "doctor", "nurse"]:
        return {
            "type": "text",
            "response": "You are not authorized to manage appointments."
        }

    return {
        "type": "buttons",
        "response": "What would you like to do?",
        "buttons": [
            {"label": "Book Appointment", "action": "book appointment"},
            {"label": "Upcoming Appointments", "action": "upcoming"},
            {"label": "Past Appointments", "action": "past"}
        ]
    }
