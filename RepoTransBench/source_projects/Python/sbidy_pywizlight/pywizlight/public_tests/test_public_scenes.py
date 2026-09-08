from pywizlight.scenes import get_scene_name_from_id

def test_scene_ids_public():
    # Use an uncommon/edge ID and confirm it returns None or similar
    assert get_scene_name_from_id(256) is None
    # Check another valid but different scene id for name
    assert get_scene_name_from_id(18) == "Candlelight"