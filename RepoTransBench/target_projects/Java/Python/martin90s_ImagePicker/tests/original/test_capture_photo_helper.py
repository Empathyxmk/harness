import pytest
import types
import os

class DummyIntent:
    pass

class DummyPackageManager:
    def __init__(self, acts):
        self.acts = acts
    def query_intent_activities(self, intent, flags):
        return self.acts

class DummyActivity:
    def __init__(self, pkg_mgr):
        self.last_intent = None
        self.last_request_code = -1
        self.pkg_mgr = pkg_mgr

    def start_activity_for_result(self, intent, request_code):
        self.last_intent = intent
        self.last_request_code = request_code

    def get_package_manager(self):
        return self.pkg_mgr

    def get_application_context(self):
        return self

class DummyFragment:
    def __init__(self, activity):
        self.last_intent = None
        self.last_request_code = None
        self._activity = activity

    def start_activity_for_result(self, intent, request_code):
        self.last_intent = intent
        self.last_request_code = request_code

    def get_activity(self):
        return self._activity

    def get_context(self):
        return self._activity

class CapturePhotoHelper:
    CAPTURE_PHOTO_REQUEST_CODE = 123

    def __init__(self, owner):
        self.owner = owner
        self._photo_file = None
        self.photo_folder = None

    def has_camera(self):
        acts = self.owner.get_package_manager().query_intent_activities(DummyIntent(), 0)
        return len(acts) > 0

    def set_photo(self, file_path):
        self._photo_file = DummyFile(file_path)

    def get_photo(self):
        return self._photo_file

    def create_photo_file(self):
        if self.photo_folder is None:
            return None
        return DummyFile(os.path.join(self.photo_folder, "temp.jpg"))

    def capture_photo(self, uri):
        if uri is None:
            return
        if hasattr(self.owner, 'start_activity_for_result'):
            self.owner.start_activity_for_result(DummyIntent(), self.CAPTURE_PHOTO_REQUEST_CODE)

class DummyFile:
    def __init__(self, path):
        self._path = path
    def get_absolute_path(self):
        return str(self._path)

import tempfile
import shutil

@pytest.fixture(scope="function")
def tmpdir_fixture():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d, ignore_errors=True)

@pytest.fixture()
def photo_helpers(tmpdir_fixture):
    # with camera = one stub, without camera = empty list
    with_camera = DummyPackageManager([object()])
    without_camera = DummyPackageManager([])
    dummy_act = DummyActivity(with_camera)
    dummy_frag = DummyFragment(dummy_act)
    return with_camera, without_camera, dummy_act, dummy_frag, tmpdir_fixture

def test_has_camera_true_and_false(photo_helpers):
    with_camera, without_camera, dummy_act, dummy_frag, _ = photo_helpers
    hp_act = CapturePhotoHelper(dummy_act)
    assert hp_act.has_camera()
    no_cam_act = DummyActivity(without_camera)
    hp_no_cam = CapturePhotoHelper(no_cam_act)
    assert not hp_no_cam.has_camera()

def test_set_photo_and_get_photo(photo_helpers):
    _, _, dummy_act, _, tmpdir = photo_helpers
    hp = CapturePhotoHelper(dummy_act)
    file_path = os.path.join(tmpdir, "abcde.jpg")
    hp.set_photo(file_path)
    fileobj = hp.get_photo()
    assert fileobj.get_absolute_path() == file_path

def test_create_photo_file_fallback(photo_helpers):
    _, _, dummy_act, _, _ = photo_helpers
    hp = CapturePhotoHelper(dummy_act)
    # Force photoFolder to None
    hp.photo_folder = None
    result = hp.create_photo_file()
    assert result is None

def test_capture_photo_with_uri(photo_helpers):
    _, _, dummy_act, dummy_frag, _ = photo_helpers
    hp_frag = CapturePhotoHelper(dummy_frag)
    uri = "content://foo/bar"
    hp_frag.capture_photo(uri)
    assert dummy_frag.last_intent is not None
    assert dummy_frag.last_request_code == CapturePhotoHelper.CAPTURE_PHOTO_REQUEST_CODE

    hp_act = CapturePhotoHelper(dummy_act)
    dummy_act.last_intent = None
    hp_act.capture_photo(uri)
    assert dummy_act.last_intent is not None
    assert dummy_act.last_request_code == CapturePhotoHelper.CAPTURE_PHOTO_REQUEST_CODE

def test_capture_photo_null_uri(photo_helpers):
    _, _, dummy_act, _, _ = photo_helpers
    hp = CapturePhotoHelper(dummy_act)
    hp.capture_photo(None)
    assert dummy_act.last_intent is None