from agentic.verification import TransactionVerifier
from agentic.notifier import MockNotifier


def test_notifier_called_for_high_value():
    notifier = MockNotifier()
    verifier = TransactionVerifier(notifier, threshold=10.0)

    tx = {"amount": 11, "currency": "USDC", "id": "tx1"}

    called = verifier.verify_transaction(tx)

    assert called is True
    assert notifier.calls == [tx]


def test_notifier_not_called_for_low_value():
    notifier = MockNotifier()
    verifier = TransactionVerifier(notifier, threshold=10.0)

    tx = {"amount": 10, "currency": "USDC", "id": "tx2"}

    called = verifier.verify_transaction(tx)

    assert called is False
    assert notifier.calls == []
