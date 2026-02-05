from typing import Dict, List

class Notifier:
    """Notifier interface for sending external approvals/alerts."""

    def notify_transaction_for_approval(self, transaction: Dict) -> None:
        raise NotImplementedError


class MockNotifier(Notifier):
    """Simple test double that records calls."""

    def __init__(self) -> None:
        self.calls: List[Dict] = []

    def notify_transaction_for_approval(self, transaction: Dict) -> None:
        self.calls.append(transaction)
