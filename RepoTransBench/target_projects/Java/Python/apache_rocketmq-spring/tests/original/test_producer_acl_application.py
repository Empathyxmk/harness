import pytest
from unittest.mock import Mock, ANY
from collections import defaultdict
from threading import Lock

class RocketMQLocalTransactionState:
    COMMIT = "COMMIT"
    ROLLBACK = "ROLLBACK"
    UNKNOWN = "UNKNOWN"

class RocketMQHeaders:
    TRANSACTION_ID = 'TRANSACTION_ID'
    TAGS = 'TAGS'
    KEYS = 'KEYS'

class ProducerACLApplication:
    def __init__(self):
        self.rocketMQTemplate = None
        self.springTransTopic = None
        self.springTopic = None

    def run(self):
        self.rocketMQTemplate.syncSend(self.springTopic, ANY)
        self.rocketMQTemplate.syncSend(self.springTopic, ANY)
        self.rocketMQTemplate.sendMessageInTransaction(self.springTransTopic, ANY, ANY)

    class TransactionListenerImpl:
        def __init__(self):
            self.transactionIndex = 0
            self.localTrans = {}

        def executeLocalTransaction(self, msg, arg):
            idx = self.transactionIndex
            if idx % 3 == 0:
                state = RocketMQLocalTransactionState.COMMIT
            elif idx % 3 == 1:
                state = RocketMQLocalTransactionState.ROLLBACK
            else:
                state = RocketMQLocalTransactionState.UNKNOWN
            self.transactionIndex += 1
            return state

        def checkLocalTransaction(self, msg):
            transId = msg['headers'].get(RocketMQHeaders.TRANSACTION_ID)
            state = self.localTrans.get(transId)
            if state == 0:
                return RocketMQLocalTransactionState.COMMIT
            elif state == 1:
                return RocketMQLocalTransactionState.ROLLBACK
            else:
                return RocketMQLocalTransactionState.UNKNOWN

def test_run():
    rocketMQTemplate = Mock()
    producerACLApplication = ProducerACLApplication()
    producerACLApplication.rocketMQTemplate = rocketMQTemplate
    producerACLApplication.springTransTopic = "aclTransTopic"
    producerACLApplication.springTopic = "aclTopic"
    rocketMQTemplate.syncSend.return_value = Mock()
    rocketMQTemplate.sendMessageInTransaction.return_value = Mock()
    producerACLApplication.run()
    assert rocketMQTemplate.syncSend.call_count >= 2
    assert rocketMQTemplate.sendMessageInTransaction.call_count >= 1

def test_transaction_listener_impl_executeLocalTransaction_commit():
    producerACLApplication = ProducerACLApplication()
    listener = producerACLApplication.TransactionListenerImpl()
    msg = {'payload': 'txMsg', 'headers': {RocketMQHeaders.TRANSACTION_ID: "tx_1"}}
    listener.transactionIndex = 0
    assert listener.executeLocalTransaction(msg, None) == RocketMQLocalTransactionState.COMMIT
    assert listener.executeLocalTransaction(msg, None) == RocketMQLocalTransactionState.ROLLBACK
    assert listener.executeLocalTransaction(msg, None) == RocketMQLocalTransactionState.UNKNOWN

def test_transaction_listener_impl_checkLocalTransaction_allcases():
    producerACLApplication = ProducerACLApplication()
    listener = producerACLApplication.TransactionListenerImpl()
    transId = "txId"
    listener.localTrans = {}
    listener.localTrans[transId] = 0
    msg = {'payload': "txMsg", 'headers': {RocketMQHeaders.TRANSACTION_ID: transId}}
    assert listener.checkLocalTransaction(msg) == RocketMQLocalTransactionState.COMMIT
    listener.localTrans[transId] = 1
    assert listener.checkLocalTransaction(msg) == RocketMQLocalTransactionState.ROLLBACK
    listener.localTrans[transId] = 2
    assert listener.checkLocalTransaction(msg) == RocketMQLocalTransactionState.UNKNOWN
    listener.localTrans.pop(transId)
    assert listener.checkLocalTransaction(msg) == RocketMQLocalTransactionState.UNKNOWN

def test_main():
    ProducerACLApplication.main = staticmethod(lambda args: None)
    ProducerACLApplication.main([])