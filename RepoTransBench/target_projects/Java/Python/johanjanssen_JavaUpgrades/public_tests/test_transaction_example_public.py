import pytest

class TransactionExample:
    def do_transaction(self):
        return "transaction completed"

def test_transactional_work_public():
    tx = TransactionExample()
    assert len(tx.do_transaction()) > 0