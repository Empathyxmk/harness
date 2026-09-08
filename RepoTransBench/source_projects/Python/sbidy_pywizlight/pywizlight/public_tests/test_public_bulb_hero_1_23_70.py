from pywizlight.bulblibrary import bulb_types

def test_bulb_hero_1_23_70_public():
    # Use a different HERO model name (fictional for public case)
    assert "HERO_PUBLIC" not in bulb_types
    # Check the existing bulb is still correct for interface, just different data
    assert bulb_types["ESP01_SHDW_12WW"].features.color is False