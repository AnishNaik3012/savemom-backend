from ..interfaces import IChatModule, ChatContext
from ..v2_logic.intents import detect_intent
from ..v2_logic.safety import check_risk
from ..v2_logic.agents.maternal import maternal_agent
from ..v2_logic.agents.appointment import appointment_agent
from ..v2_logic.agents.report import report_agent
from ..v2_logic.agents.prescription import prescription_agent
from ..v2_logic.agents.lab import lab_agent
from ..v2_logic.agents.fallback import fallback_agent

class V2ChatModule(IChatModule):
    @property
    def name(self) -> str:
        return "V2_Orchestrator"

    def can_handle(self, context: ChatContext) -> bool:
        # This module handles everything in the new design
        return True

    def process(self, context: ChatContext) -> any:
        text = context.message_text
        role = context.user_role
        
        # 1. Safety Check
        safety_response = check_risk(text)
        if safety_response:
            return {"type": "text", "response": safety_response}

        # 2. Intent Detection
        intent = detect_intent(text)
        
        # 3. Route to specific agent
        if intent == "APPOINTMENT":
            return appointment_agent(text, role)
        elif intent == "REPORT":
            return report_agent(text, role)
        elif intent == "PRESCRIPTION":
            return prescription_agent(text, role)
        elif intent == "LAB":
            return lab_agent(text, role)
        elif intent == "MATERNAL_CARE":
            return maternal_agent(text, role)
        else:
            return fallback_agent(text)
