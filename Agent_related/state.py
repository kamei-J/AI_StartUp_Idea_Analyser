from typing import TypedDict

class AgentState(TypedDict):
    user_input: str
    startup_idea: str
    market_analysis: str
    competitor_analysis: str
    business_model_analysis: str
    final_report: str
    fact_check_report: str