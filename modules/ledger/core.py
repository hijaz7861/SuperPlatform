from decimal import Decimal


class Ledger:

    def __init__(self):
        self.entries = []

    def post(self, account, amount, description):
        amount = Decimal(str(amount))

        self.entries.append({
            "account": account,
            "amount": amount,
            "description": str(description),
        })

    def balance(self, account):
        total = Decimal("0")

        for entry in self.entries:
            if entry["account"] == account:
                total += entry["amount"]

        return total

    def contains_interest(self):
        keywords = (
            "interest",
            "riba",
            "usury",
        )

        for entry in self.entries:
            text = entry["description"].lower()

            if any(word in text for word in keywords):
                return True

        return False
