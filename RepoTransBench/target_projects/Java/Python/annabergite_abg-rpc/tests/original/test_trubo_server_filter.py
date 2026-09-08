class Request:
    def __init__(self):
        self.tracer = None
    def getTracer(self):
        return self.tracer

class Response:
    def __init__(self):
        self.tracer = None
    def setTracer(self, tracer):
        self.tracer = tracer

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
    def setTracer(tracer):
        pass

class RpcServerFilter:
    def onSend(self, request, response):
        tracer = request.getTracer()
        if tracer is not None:
            RemoteContext.getClientAddress()
            RemoteContext.getServerAddress()
            RemoteContext.getServiceMethodName()
            TracerContext.setTracer(tracer)
            response.setTracer(tracer)
    def onRecive(self, request):
        return True
    def onError(self, request, response, throwable):
        pass

class abgServer:
    def __init__(self):
        self.filters = []
    def addFirst(self, filter_inst):
        self.filters.insert(0, filter_inst)

class TruboServerFilterTest:
    def setabgServer(self, abgServer_inst):
        abgServer_inst.addFirst(RpcServerFilter())

def test_trubo_server_filter():
    abg_server = abgServer()
    f = TruboServerFilterTest()
    f.setabgServer(abg_server)
    req = Request()
    res = Response()
    abg_server.filters[0].onSend(req, res)
    assert abg_server.filters[0].onRecive(req)