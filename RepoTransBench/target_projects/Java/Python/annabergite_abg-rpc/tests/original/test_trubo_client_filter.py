class Request:
    def __init__(self):
        self.tracer = None
    def setTracer(self, tracer):
        self.tracer = tracer

class Response:
    pass

class Tracer:
    pass

class RemoteContext:
    @staticmethod
    def getClientAddress():
        return "client"
    @staticmethod
    def getServerAddress():
        return "server"
    @staticmethod
    def getServiceMethodName():
        return "method"

class TracerContext:
    @staticmethod
    def nextTracer():
        return Tracer()

class RpcClientFilter:
    def onSend(self, request):
        tracer = TracerContext.nextTracer()
        if tracer is not None:
            RemoteContext.getClientAddress()
            RemoteContext.getServerAddress()
            RemoteContext.getServiceMethodName()
            request.setTracer(tracer)
        return True
    def onRecive(self, request, response):
        pass
    def onError(self, request, response, throwable):
        pass

class abgClient:
    def __init__(self):
        self.filters = []
    def addFirst(self, filter_inst):
        self.filters.insert(0, filter_inst)

class TruboClientFilterTest:
    def setabgClient(self, abgClient_inst):
        abgClient_inst.addFirst(RpcClientFilter())

def test_trubo_client_filter():
    abg_client = abgClient()
    f = TruboClientFilterTest()
    f.setabgClient(abg_client)
    # Ensure filter can be called
    req = Request()
    assert abg_client.filters[0].onSend(req)