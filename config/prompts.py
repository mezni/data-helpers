"""Prompt templates for the specialist agents.

Loaded via src/llm/prompt_manager.py (PromptManager.get_prompt(name)).
Templates are empty for now; fill in system / user_template per agent.

Prompt keys follow config/prompts.yaml.txt from the reference bootcamp:
customer_profile_prompt, credit_risk_prompt, compliance_prompt,
lending_policy_prompt, recommendation_prompt.
"""

PROMPTS = {
    "customer_profile_prompt": {
        "system": "",
        "user_template": "",
    },
    "credit_risk_prompt": {
        "system": "",
        "user_template": "",
    },
    "compliance_prompt": {
        "system": "",
        "user_template": "",
    },
    "lending_policy_prompt": {
        "system": "",
        "user_template": "",
    },
    "recommendation_prompt": {
        "system": "",
        "user_template": "",
    },
}