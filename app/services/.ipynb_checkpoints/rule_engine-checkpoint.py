from typing import List


class RuleEngine:

    @staticmethod
    def merge_rules(system_rules: List[str], user_rules: List[str]):

        seen = set()
        final = []

        # system rules first (higher priority)
        for r in system_rules:
            key = r.lower().strip()
            if key not in seen:
                seen.add(key)
                final.append(f"[SYSTEM] {r}")

        # user rules next
        for r in user_rules:
            key = r.lower().strip()
            if key not in seen:
                seen.add(key)
                final.append(f"[USER] {r}")

        return final