import os
import sys

# Add the prescription module to sys.path
# Assuming the root of the project is two levels up from this agent
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
presc_module_path = os.path.join(project_root, "presc_hybrid/presc_hybrid")

if presc_module_path not in sys.path:
    sys.path.append(presc_module_path)

try:
    from src.analyzer import PrescriptionAnalyzer
    analyzer = PrescriptionAnalyzer()
except Exception as e:
    print(f"CRITICAL ERROR importing PrescriptionAnalyzer: {e}")
    import traceback
    traceback.print_exc()
    analyzer = None

def prescription_agent(message: str, user_role: str):
    """
    Handles queries about prescriptions and medicines.
    Interfaces with the PrescriptionAnalyzer from presc_hybrid.
    """
    msg = message.lower()
    
    if not analyzer:
         print("DEBUG: Analyzer is None, returning unavailable message.")
         return {
            "type": "text",
            "response": "The prescription analysis module is currently unavailable due to a system configuration error. Please contact support."
        }

    if "analyze" in msg or "upload" in msg or "check" in msg:
        return {
            "type": "buttons",
            "response": "I can help you analyze your prescription. Please upload an image or PDF of your prescription.",
            "buttons": [
                {"label": "📤 Upload Prescription", "action": "upload_prescription"}
            ]
        }
    
    # Simple direct question handling (can be expanded)
    if any(word in msg for word in ["what", "how", "side effects", "dosage"]):
        # This could call analyzer.ask_medical_question if we had context
        # For now, we'll prompt for the upload first to get context.
        return {
            "type": "text",
            "response": "To give you accurate information about your medications, I first need to see your prescription. Please use the 'Upload Prescription' option to get started."
        }

    return {
        "type": "buttons",
        "response": "How can I help you with your prescriptions today?",
        "buttons": [
            {"label": "📤 Upload Prescription", "action": "upload_prescription"},
            {"label": "📋 My Medicines", "action": "view_medicines"}
        ]
    }
