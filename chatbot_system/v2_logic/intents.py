import sys
import os

# Ensure the app root is in path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

try:
    from lab.nlp import nlp_service as lab_nlp
except ImportError:
    lab_nlp = None

def detect_intent(text: str) -> str:
    """
    Detect user intent from message text
    """
    if not text:
        return "UNKNOWN"

    text = text.lower()
    print(f"DEBUG: Detecting intent for: {text}")

    # 1. Try Lab NLP Model if available
    if lab_nlp:
        intent, confidence = lab_nlp.predict_intent(text)
        if intent != "None" and confidence > 0.65:
            print(f"DEBUG: Lab NLP detected: {intent} ({confidence:.2f})")
            return "LAB" # Return LAB to maintain routing, but we can also return specialized intents if needed

    appointment_keywords = [
        "appointment",
        "book",
        "schedule",
        "doctor visit",
        "checkup",
        "upcoming"
    ]

    maternal_keywords = [
        "pregnancy",
        "pregnant",
        "diet",
        "food",
        "pain",
        "cramps",
        "baby",
        "weeks"
    ]

    report_keywords = [
        "report",
        "medical record",
        "lab results",
        "patient reports",
        "reports",
        "summary",
        "get summary"
    ]

    prescription_keywords = [
        "prescription",
        "medicine list",
        "meds",
        "medicine names",
        "analyze prescription",
        "pills",
        "dosage",
        "manage prescriptions",
        "manage",
        "my prescriptions"
    ]

    lab_keywords = [
        "lab",
        "blood test",
        "sugar level",
        "hemoglobin",
        "test results",
        "glucose",
        "investigation",
        "thyroid",
        "urine test"
    ]

    if any(keyword in text for keyword in lab_keywords):
        return "LAB"

    if any(keyword in text for keyword in appointment_keywords):
        return "APPOINTMENT"

    if any(keyword in text for keyword in report_keywords):
        return "REPORT"

    if any(keyword in text for keyword in prescription_keywords):
        print("DEBUG: Intent detected as PRESCRIPTION")
        return "PRESCRIPTION"

    if any(keyword in text for keyword in maternal_keywords):
        return "MATERNAL_CARE"

    return "UNKNOWN"
