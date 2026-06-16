def load_default_rules():
    with open("app/data/rules/insurance_rules.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]