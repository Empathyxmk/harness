def test_public_prototype_property_inheritance(capsys):
    class Shape:
        color = "red"  # Class variable acts like prototype property
        def __init__(self):
            self.kind = "shape"
    s = Shape()
    print(f"{s.kind}, {Shape.color}")
    captured = capsys.readouterr()
    assert "shape, red" in captured.out.strip()