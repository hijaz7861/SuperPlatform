"""Calculate charges for problem solutions."""
BASE_RATES = {
    "code_bug": 25,
    "code_request": 40,
    "tech_support": 15,
    "design": 35,
    "data": 30,
    "general": 20,
}


class PricingEngine:
    def __init__(self, hourly_rate_override=None):
        self.hourly_rate_override = hourly_rate_override

    def calculate(self, problem, solution):
        category = problem.get("category", "general")
        hours = solution.get("estimated_hours", 2)
        rate = self.hourly_rate_override or BASE_RATES.get(category, 20)
        amount = rate * hours
        return {"amount": amount, "rate": rate, "hours": hours, "currency": "USD"}

    def calculate_batch(self, problems, solutions):
        return [self.calculate(p, s) for p, s in zip(problems, solutions)]
