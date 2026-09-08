import pytest

class Bundle(dict):
    pass

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

class EasyGcmStubberPublic:
    calledOnMessage = False

    @staticmethod
    def setGcmListenerSpy():
        class GcmListenerSpy(GcmListener):
            def onMessage(self_inner, from_addr, data):
                if from_addr == "public_sender" and data.get("another_key") == "another_value":
                    EasyGcmStubberPublic.calledOnMessage = True
        EasyGcm.getInstance().setGcmListener(GcmListenerSpy())

    @staticmethod
    def reset():
        EasyGcmStubberPublic.calledOnMessage = False

def test_on_message_received_delegates_to_easygcm_different():
    from_addr = "public_sender"
    data = Bundle()
    data["another_key"] = "another_value"
    EasyGcmStubberPublic.setGcmListenerSpy()
    service = EasyGcmListenerService()
    service.onMessageReceived(from_addr, data)
    assert EasyGcmStubberPublic.calledOnMessage
    EasyGcmStubberPublic.reset()