from typing import Dict
from .notifier import Notifier


class TransactionVerifier:
    """Verifies transactions and notifies humans when approval is required.

    By default it checks for transactions in `USDC` above the configured threshold.
    """

    def __init__(self, notifier: Notifier, threshold: float = 10.0, currency: str = "USDC") -> None:
        self.notifier = notifier
        self.threshold = float(threshold)
        self.currency = currency

    def verify_transaction(self, transaction: Dict) -> bool:
        """Return True if a notification was sent (i.e., approval required).

        Non-numeric or missing amounts are treated as zero.
        """
        try:
            amt = float(transaction.get("amount", 0))
        except (TypeError, ValueError):
            amt = 0.0

        if transaction.get("currency") == self.currency and amt > self.threshold:
            self.notifier.notify_transaction_for_approval(transaction)
            return True
        return False
