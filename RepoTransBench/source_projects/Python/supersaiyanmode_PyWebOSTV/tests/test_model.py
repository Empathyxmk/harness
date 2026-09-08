import pytest
from pywebostv import model

def test_application_repr_and_eq():
    app_data_1 = {"appId": "youtube.leanback.v4", "title": "YouTube", "icon": "icon_url"}
    app_data_2 = {"appId": "youtube.leanback.v4", "title": "YouTube", "icon": "icon_url"}
    app_data_3 = {"appId": "test.other.app", "title": "Test App", "icon": "icon_url2"}

    app1 = model.Application(app_data_1)
    app2 = model.Application(app_data_1)  # Use same dict to test equality semantics
    app3 = model.Application(app_data_3)

    assert isinstance(repr(app1), str)
    assert app1 == app1
    assert app1 != app2
    assert app1 != app3
    assert app1 != 123  # eq different type

def test_application_getitem_and_missing():
    app_data = {"appId": "netflix", "title": "Netflix", "icon": "icon"}
    app = model.Application(app_data)
    assert app["appId"] == "netflix"
    with pytest.raises(KeyError):
        _ = app["nonexistent"]

def test_input_source_repr_and_eq():
    src_data_1 = {"label": "HDMI 1", "id": "HDMI_1"}
    src_data_2 = {"label": "HDMI 1", "id": "HDMI_1"}
    src_data_3 = {"label": "HDMI 2", "id": "HDMI_2"}

    src1 = model.InputSource(src_data_1)
    src2 = model.InputSource(src_data_1)  # Use same dict for equality semantics consistency
    src3 = model.InputSource(src_data_3)

    assert isinstance(repr(src1), str)
    assert src1 == src1
    assert src1 != src2
    assert src1 != src3
    assert src1 != "foo"  # eq different type

def test_input_source_fields():
    src_data = {"label": "HDMI 1", "id": "HDMI_1"}
    src = model.InputSource(src_data)
    assert src.label == "HDMI 1"
    # Instead of src._src["id"], test that subscripting works properly
    assert src["id"] == "HDMI_1"
    with pytest.raises(KeyError):
        _ = src["nonexistent"]

@pytest.mark.skipif(not hasattr(model, "TVChannel"), reason="TVChannel not implemented in pywebostv.model")
def test_tv_channel_repr_and_eq():
    ch_data_1 = {"channelId": "100", "channelName": "BBC"}
    ch_data_2 = {"channelId": "100", "channelName": "BBC"}
    ch_data_3 = {"channelId": "101", "channelName": "CNN"}

    ch1 = model.TVChannel(ch_data_1)
    ch2 = model.TVChannel(ch_data_1)
    ch3 = model.TVChannel(ch_data_3)

    assert isinstance(repr(ch1), str)
    assert ch1 == ch1
    assert ch1 != ch2
    assert ch1 != ch3
    assert ch1 != object()  # eq different type

@pytest.mark.skipif(not hasattr(model, "TVChannelProgram"), reason="TVChannelProgram not implemented in pywebostv.model")
def test_tv_channel_program_eq_and_repr():
    prog_data_1 = {"programTitle": "My Show"}
    prog_data_2 = {"programTitle": "My Show"}
    prog_data_3 = {"programTitle": "Another Show"}

    prog1 = model.TVChannelProgram(prog_data_1)
    prog2 = model.TVChannelProgram(prog_data_1)
    prog3 = model.TVChannelProgram(prog_data_3)

    assert prog1 == prog1
    assert prog1 != prog2
    assert prog1 != prog3
    assert isinstance(repr(prog1), str)
    assert prog1 != "Show"  # eq with different type

def test_repr_edgecases():
    # Application with minimal data
    app = model.Application({"title": "Minimal"})
    r = repr(app)
    assert "<Application" in r

    # InputSource with minimal data
    src = model.InputSource({"label": "L", "id": "I"})
    r = repr(src)
    assert "<InputSource" in r