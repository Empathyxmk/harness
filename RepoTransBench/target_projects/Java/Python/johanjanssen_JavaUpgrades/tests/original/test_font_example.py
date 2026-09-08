import pytest

class FontExample:
    def create_work_book(self):
        # Simulate workbook creation
        pass

def test_create_work_book():
    font_example = FontExample()
    font_example.create_work_book()

def test_list_fonts():
    # Simulate listing fonts
    names = ["Arial", "Times New Roman", "Courier New"]
    print(f"Found {len(names)} fonts:")
    for name in names:
        print(name)

def test_example():
    import openpyxl
    workbook = openpyxl.Workbook()
    sheet = workbook.create_sheet("Asset requests")