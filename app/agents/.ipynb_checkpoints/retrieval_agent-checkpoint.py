from app.services.rule_loader import load_default_rules
from app.services.rule_engine import RuleEngine


class RetrievalAgent:

    @staticmethod
    def retrieve(document_text: str, uploaded_rules=None):

        """
        Retrieves and merges rules from:
        1. System default rules (rules.txt)
        2. User uploaded rules (optional)
        """

        # ----------------------------
        # STEP 1: LOAD SYSTEM RULES
        # ----------------------------
        system_rules = load_default_rules()

        # ----------------------------
        # STEP 2: LOAD USER RULES
        # ----------------------------
        user_rules = uploaded_rules if uploaded_rules else []

        # ----------------------------
        # STEP 3: VALIDATION SAFETY
        # ----------------------------
        if not isinstance(user_rules, list):
            user_rules = []

        # ----------------------------
        # STEP 4: MERGE RULES (ENTERPRISE LOGIC)
        # ----------------------------
        final_rules = RuleEngine.merge_rules(
            system_rules,
            user_rules
        )

        # ----------------------------
        # OPTIONAL: DEBUG LOGGING
        # ----------------------------
        print("\n📚 RULE RETRIEVAL SUMMARY")
        print(f"System Rules: {len(system_rules)}")
        print(f"User Rules: {len(user_rules)}")
        print(f"Final Rules: {len(final_rules)}")

        return final_rules