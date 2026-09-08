import pytest
from jaydenseric_apollo_upload_client.formDataAppendFile import formDataAppendFile

class FakeFormData:
    def __init__(self):
        self.appended_field = None
        self.appended_file = None
        self.appended_file_name = None

    def append(self, field, file, file_name):
        self.appended_field = field
        self.appended_file = file
        self.appended_file_name = file_name

def test_formDataAppendFile_public():
    # Public: use different data!
    fake_form_data = FakeFormData()
    field = 'avatar'
    file = {'type': 'image/png', 'content': 'PNGDATA'}
    file_name = 'avatar-2024.png'

    formDataAppendFile(fake_form_data, field, file, file_name)
    assert fake_form_data.appended_field == field, "Field should match"
    assert fake_form_data.appended_file == file, "File object should match"
    assert fake_form_data.appended_file_name == file_name, "File name should match"