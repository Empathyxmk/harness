import pytest
from src.devicelist import (
    DeviceItem, AddItemToList, GetItemFromList, RemoveItemFromList,
    IsItemAlreadyStored, CopyElement, CreateFilteredList, DeviceParams, ListResultItem, clear_all_devices
)

# Helper to create and fill a DeviceItem for public tests with DIFFERENT data
def createDevice_public(key, loc=10, vid=2222, pid=3333):
    item = DeviceItem()
    item.deviceParams.locationId = loc
    item.deviceParams.vendorId = vid
    item.deviceParams.productId = pid
    item.deviceParams.deviceName = "PublicDevice"
    item.deviceParams.manufacturer = "PublicMaker"
    item.deviceParams.serialNumber = "XYZ789"
    item.deviceParams.deviceAddress = 15
    item.SetKey(key)
    return item

def test_add_and_get_item_public():
    clear_all_devices()
    item = createDevice_public("pub1")
    AddItemToList("pub1", item)
    result = GetItemFromList("pub1")
    assert result is not None
    assert result.deviceParams.locationId == 10
    # Returns None for missing keys (different key from original tests)
    assert GetItemFromList("pub_missing") is None

def test_remove_item_from_list_public():
    clear_all_devices()
    item = createDevice_public("pub_remove")
    AddItemToList("pub_remove", item)
    assert GetItemFromList("pub_remove") is not None
    RemoveItemFromList(item)
    assert GetItemFromList("pub_remove") is None

def test_is_item_already_stored_public():
    clear_all_devices()
    item = createDevice_public("pub_exist")
    AddItemToList("pub_exist", item)
    assert IsItemAlreadyStored("pub_exist")
    assert not IsItemAlreadyStored("pub_nonexist")

def test_copy_element_public():
    clear_all_devices()
    item = createDevice_public("pub_copy")
    cpy = CopyElement(item.deviceParams)
    assert cpy.locationId == item.deviceParams.locationId
    assert cpy.vendorId == item.deviceParams.vendorId
    assert cpy.productId == item.deviceParams.productId
    assert cpy.deviceName == item.deviceParams.deviceName
    assert cpy.manufacturer == item.deviceParams.manufacturer
    assert cpy.serialNumber == item.deviceParams.serialNumber
    assert cpy.deviceAddress == item.deviceParams.deviceAddress

def test_create_filtered_list_public():
    clear_all_devices()
    # Add two devices of different VIDs/PIDs
    item1 = createDevice_public("pubflt1", 10, 2345, 6789)
    item2 = createDevice_public("pubflt2", 20, 2345, 9870)
    AddItemToList("pubflt1", item1)
    AddItemToList("pubflt2", item2)

    filteredList = []

    # Filter by vendor+product
    CreateFilteredList(filteredList, 2345, 6789)
    assert len(filteredList) == 1
    filteredList.clear()

    # Filter by vendor only
    CreateFilteredList(filteredList, 2345, 0)
    assert len(filteredList) == 2
    filteredList.clear()

    # Filter by no filter (should return all)
    CreateFilteredList(filteredList, 0, 0)
    assert len(filteredList) >= 2