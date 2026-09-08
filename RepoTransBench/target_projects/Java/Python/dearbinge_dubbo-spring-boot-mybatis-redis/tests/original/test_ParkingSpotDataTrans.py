import pytest
from unittest.mock import Mock, MagicMock, patch, ANY
from io import StringIO

# Simulated target classes
class InfrastructDeal:
    def accept(self, request):
        pass

class SecurityService:
    pass

class ParkingSpotDataTrans:
    def __init__(self):
        self.posDataServiceMap = {}
        self.securityService = None

    def getSession(self, request, response):
        session = request.getSession()
        if session is None:
            return
        session.setAttribute("username", "chubin")
        sessionid = session.getId()
        try:
            w = response.getWriter()
            w.write(f"node3 sessionid:{sessionid}")
        except Exception as e:
            pass

    def getUserName(self, request, response):
        session = request.getSession()
        w = response.getWriter()
        if not session:
            w.write("no session found")
            return
        username = session.getAttribute("username")
        if username is None:
            w.write("no attribute found")
            return
        w.write(str(username))

    def create(self, request, response):
        method = request.getParameter("method")
        if method not in self.posDataServiceMap:
            # No handler present: do nothing, no output
            return
        deal = self.posDataServiceMap[method]
        try:
            result = deal.accept(request)
            w = response.getWriter()
            w.write(result)
        except Exception as e:
            raise

    def addInterceptors(self, registry):
        registry.addInterceptor(ANY)

@pytest.fixture
def fake_controller():
    ctrl = ParkingSpotDataTrans()
    ctrl.posDataServiceMap = {}
    ctrl.securityService = MagicMock(spec=SecurityService)
    return ctrl

@pytest.fixture
def fake_request():
    req = MagicMock(name='HttpServletRequest')
    sess = MagicMock(name='HttpSession')
    req.getSession.return_value = sess
    req.getParameter.side_effect = lambda key: None
    return req

@pytest.fixture
def fake_response():
    resp = MagicMock(name='HttpServletResponse')
    writer_buffer = StringIO()
    writer = MagicMock()
    writer.write.side_effect = writer_buffer.write
    writer.flush.side_effect = lambda: None
    resp.getWriter.return_value = writer
    resp._writer_buffer = writer_buffer
    return resp

def test_get_session_normal(fake_controller, fake_request, fake_response):
    session = fake_request.getSession.return_value
    session.getId.return_value = "abcde12345"
    fake_controller.getSession(fake_request, fake_response)
    session.setAttribute.assert_called_with("username", "chubin")
    fake_response.getWriter().flush()
    val = fake_response._writer_buffer.getvalue()
    assert "node3" in val
    assert "sessionid:abcde12345" in val

def test_get_session_ioexception(fake_controller, fake_request, fake_response):
    # Patch getWriter to raise an exception
    fake_response.getWriter.side_effect = Exception("write error")
    fake_controller.getSession(fake_request, fake_response)
    # Should not raise

def test_get_username_no_session(fake_controller, fake_request, fake_response):
    fake_request.getSession.return_value = None
    fake_response._writer_buffer = StringIO()
    fake_writer = MagicMock()
    fake_writer.write.side_effect = fake_response._writer_buffer.write
    fake_writer.flush.side_effect = lambda: None
    fake_response.getWriter.return_value = fake_writer
    fake_controller.getUserName(fake_request, fake_response)
    fake_writer.flush()
    assert "no session found" in fake_response._writer_buffer.getvalue()

def test_get_username_no_attribute(fake_controller, fake_request, fake_response):
    session = fake_request.getSession.return_value
    session.getAttribute.return_value = None
    fake_controller.getUserName(fake_request, fake_response)
    fake_response.getWriter().flush()
    assert "no attribute found" in fake_response._writer_buffer.getvalue()

def test_get_username_with_username(fake_controller, fake_request, fake_response):
    session = fake_request.getSession.return_value
    session.getAttribute.return_value = "testuser"
    fake_controller.getUserName(fake_request, fake_response)
    fake_response.getWriter().flush()
    assert "testuser" in fake_response._writer_buffer.getvalue()

def test_get_username_ioexception(fake_controller, fake_request, fake_response):
    # getWriter should raise
    fake_response.getWriter.side_effect = Exception("fail")
    with pytest.raises(Exception):
        fake_controller.getUserName(fake_request, fake_response)

def test_create_no_ideal(fake_controller, fake_request, fake_response):
    fake_request.getParameter.return_value = "notexist"
    fake_controller.create(fake_request, fake_response)
    fake_response.getWriter().flush()
    # No output expected
    assert fake_response._writer_buffer.getvalue() == ""

def test_create_with_ideal(fake_controller, fake_request, fake_response):
    method_name = "sync"
    deal = MagicMock(spec=InfrastructDeal)
    deal.accept.return_value = "ok"
    fake_controller.posDataServiceMap[method_name] = deal
    fake_request.getParameter.return_value = method_name

    fake_controller.create(fake_request, fake_response)
    deal.accept.assert_called_once_with(fake_request)
    fake_response.getWriter().flush()
    assert fake_response._writer_buffer.getvalue() == "ok"

def test_create_ideal_throws(fake_controller, fake_request, fake_response):
    method_name = "sync"
    deal = MagicMock(spec=InfrastructDeal)
    deal.accept.side_effect = RuntimeError("fail")
    fake_controller.posDataServiceMap[method_name] = deal
    fake_request.getParameter.return_value = method_name

    with pytest.raises(Exception):
        fake_controller.create(fake_request, fake_response)

def test_add_interceptors_coverage(fake_controller):
    registry = MagicMock()
    registry.addInterceptor.return_value = MagicMock()
    fake_controller.addInterceptors(registry)
    assert registry.addInterceptor.call_count == 1