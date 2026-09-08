from easy_thumbnails.widgets import ClearableFileInputWithInitial

def test_clearable_file_input_initial_text_public():
    widget = ClearableFileInputWithInitial()
    # Use different label than default
    widget.initial_text = "originally_uploaded"
    assert widget.initial_text == "originally_uploaded"

def test_clearable_file_input_template_name_public():
    widget = ClearableFileInputWithInitial()
    # Template name check
    assert "clearable" in widget.template_name