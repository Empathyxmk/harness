import pytest

class PickerConfig:
    def __init__(self, ctx):
        self.ctx = ctx
    def get_app_context(self):
        return self.ctx

class DummyConfig(PickerConfig):
    def __init__(self, ctx):
        super().__init__(ctx)

class DummyActivity:
    def __init__(self):
        self.last_intent = None
        self.last_request_code = None
    def start_activity_for_result(self, intent, request_code):
        self.last_intent = intent
        self.last_request_code = request_code

class DummyFragment:
    def __init__(self, act):
        self.act = act
        self.last_intent = None
        self.last_request_code = None
    def get_activity(self):
        return self.act
    def get_context(self):
        return self.act
    def start_activity_for_result(self, intent, request_code):
        self.last_intent = intent
        self.last_request_code = request_code

class SImagePicker:
    picker_config = None

    @classmethod
    def init(cls, config):
        cls.picker_config = config

    @classmethod
    def get_picker_config(cls):
        if cls.picker_config is None:
            raise ValueError("Picker config not initialized!")
        return cls.picker_config

    @classmethod
    def from_(cls, obj):
        cls.get_picker_config()
        return cls(obj)

    def __init__(self, obj):
        self.owner = obj

    def max_count(self, count):
        return self
    def row_count(self, count):
        return self
    def pick_mode(self, mode):
        return self
    def crop_file_path(self, path):
        return self
    def show_camera(self, yesno):
        return self
    def pick_text(self, x):
        return self
    def set_selected(self, selected):
        return self
    def for_result(self, code):
        if isinstance(self.owner, DummyActivity):
            self.owner.start_activity_for_result("dummy", code)
        elif isinstance(self.owner, DummyFragment):
            self.owner.start_activity_for_result("dummy", code)
        else:
            raise ValueError("Neither activity nor fragment")
    def file_interceptor(self, interceptor):
        return self

SImagePicker.MODE_AVATAR = "avatar"
SImagePicker.MODE_IMAGE = "image"

@pytest.fixture
def simage_setup():
    dummy_activity = DummyActivity()
    dummy_fragment = DummyFragment(dummy_activity)
    SImagePicker.init(DummyConfig(dummy_activity))
    return dummy_activity, dummy_fragment

def test_get_picker_config_exception_if_not_initialized(simage_setup):
    dummy_activity, _ = simage_setup
    SImagePicker.picker_config = None
    with pytest.raises(ValueError):
        SImagePicker.get_picker_config()

def test_for_result_no_init_throws(simage_setup):
    dummy_activity, _ = simage_setup
    SImagePicker.picker_config = None
    with pytest.raises(ValueError):
        SImagePicker.from_(dummy_activity).for_result(1)

def test_from_activity_and_from_fragment(simage_setup):
    dummy_activity, dummy_fragment = simage_setup
    SImagePicker.init(DummyConfig(dummy_activity))
    picker1 = SImagePicker.from_(dummy_activity)
    assert picker1 is not None
    picker2 = SImagePicker.from_(dummy_fragment)
    assert picker2 is not None

def test_max_count_row_count_pick_mode_crop_file_show_camera_pick_text_set_selected(simage_setup):
    dummy_activity, _ = simage_setup
    picker = SImagePicker.from_(dummy_activity)
    selected = []
    picker.max_count(5).row_count(2).pick_mode(SImagePicker.MODE_AVATAR)\
        .crop_file_path("test.jpg").show_camera(True).pick_text(123)\
        .set_selected(selected)

def test_for_result_calls_activity_and_fragment(simage_setup):
    dummy_activity, dummy_fragment = simage_setup
    pickerA = SImagePicker.from_(dummy_activity)
    pickerA.for_result(99)
    assert dummy_activity.last_intent is not None
    assert dummy_activity.last_request_code == 99

    pickerF = SImagePicker.from_(dummy_fragment)
    pickerF.for_result(66)
    assert dummy_fragment.last_intent is not None
    assert dummy_fragment.last_request_code == 66

def test_for_result_neither_activity_nor_fragment(simage_setup):
    class BadPicker(SImagePicker):
        pass
    bad = SImagePicker(None)
    SImagePicker.init(DummyConfig(simage_setup[0]))
    with pytest.raises(ValueError):
        bad.for_result(7)

def test_file_interceptor(simage_setup):
    dummy_activity, _ = simage_setup
    picker = SImagePicker.from_(dummy_activity)
    picker.file_interceptor(None)