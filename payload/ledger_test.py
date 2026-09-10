import sys
from pathlib import Path
from decimal import Decimal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modules.ledger.core import Ledger

ledger = Ledger()

ledger.post(
    "cash",
    "1000",
    "capital contribution"
)

ledger.post(
    "cash",
    "-250",
    "operating expense"
)

assert ledger.balance("cash") == Decimal("750")
assert ledger.contains_interest() is False

print("DEBIT/CREDIT BALANCE TEST: PASS")
print("NO-INTEREST POLICY TEST: PASS")
print("RIBA-FREE LEDGER: PASS")
