import pytest

class Bundle(dict):
    pass

# Emulates the GcmListener interface and EasyGcm singleton
class GcmListener:
    def onMessage(self, from_addr, data):
        pass

class EasyGcm:
    _instance = None
    _listener = None

    @staticmethod
    def getInstance():
        if EasyGcm._instance is None:
            EasyGcm._instance = EasyGcm()
        return EasyGcm._instance

    def setGcmListener(self, listener):
        EasyGcm._listener = listener

    def getGcmListener(self):
        return EasyGcm._listener

class EasyGcmListenerService:
    def onMessageReceived(self, from_addr, data):
        listener = EasyGcm.getInstance().getGcmListener()
        if listener is not None:
            listener.onMessage(from_addr, data)

class EasyGcmStubber:
    calledOnMessage = False

    @staticmethod
    def setGcmListenerSpy():
        class GcmListenerSpy(GcmListener):
            def onMessage(self, from_addr, data):
                EasyGcmStubber.calledOnMessage = True
        EasyGcm.getInstance().setGcmListener(GcmListenerSpy())

    @staticmethod
    def reset():
        EasyGcmStubber.calledOnMessage = False

def test_on_message_received_delegates_to_easygcm():
    from_addr = "sender"
    data = Bundle()
    data["key"] = "value"

    EasyGcmStubber.setGcmListenerSpy()

    service = EasyGcmListenerService()
    service.onMessageReceived(from_addr, data)

    assert EasyGcmStubber.calledOnMessage
    EasyGcmStubber.reset()