class Gui:
    def __init__(self):
        pass

def test_basic_gui_instantiation():
    try:
        gui = Gui()
        assert gui is not None
    except Exception as e:
        assert False, f"Gui instantiation failed: {e}"