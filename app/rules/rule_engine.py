class RuleEngine:
    def evaluate(self, txn):
        rules = []

        # Rule 1: High amount
        if txn.amount > 5000:
            rules.append("HIGH_AMOUNT")

        # (Optional future rules can be added later)
        return rules
