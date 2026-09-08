import pytest
from src.devicelist import (
    DeviceItem, AddItemToList, GetItemFromList, RemoveItemFromList,
    IsItemAlreadyStored, CopyElement, CreateFilteredList, DeviceParams, ListResultItem, clear_all_devices
)

# Helper to create and fill a DeviceItem for tests
def createDevice(key, loc=1, vid=1111, pid=2222):
    item = DeviceItem()
    item.deviceParams.locationId = loc
    item.deviceParams.vendorId = vid
    item.deviceParams.productId = pid
    item.deviceParams.deviceName = "TestDevice"
    item.deviceParams.manufacturer = "TestMaker"
    item.deviceParams.serialNumber = "ABC123"
    item.deviceParams.deviceAddress = 5
    item.SetKey(key)
    return item

def test_add_and_get_item():
    clear_all_devices()
    item = createDevice("dev1")
    AddItemToList("dev1", item)
    result = GetItemFromList("dev1")
    assert result is not None
    assert result.deviceParams.locationId == 1
    # Returns None for missing keys
    assert GetItemFromList("dev_missing") is None

def test_remove_item_from_list():
    clear_all_devices()
    item = createDevice("dev_remove")
    AddItemToList("dev_remove", item)
    assert GetItemFromList("dev_remove") is not None
    RemoveItemFromList(item)
    assert GetItemFromList("dev_remove") is None

def test_is_item_already_stored():
    clear_all_devices()
    item = createDevice("dev_exist")
    AddItemToList("dev_exist", item)
    assert IsItemAlreadyStored("dev_exist")
    assert not IsItemAlreadyStored("dev_nonexist")

def test_copy_element():
    clear_all_devices()
    item = createDevice("dev_copy")
    cpy = CopyElement(item.deviceParams)
    assert cpy.locationId == item.deviceParams.locationId
    assert cpy.vendorId == item.deviceParams.vendorId
    assert cpy.productId == item.deviceParams.productId
    assert cpy.deviceName == item.deviceParams.deviceName
    assert cpy.manufacturer == item.deviceParams.manufacturer
    assert cpy.serialNumber == item.deviceParams.serialNumber
    assert cpy.deviceAddress == item.deviceParams.deviceAddress

def test_create_filtered_list():
    clear_all_devices()
    # Add two devices of different VIDs/PIDs
    item1 = createDevice("devflt1", 1, 1234, 5678)
    item2 = createDevice("devflt2", 2, 1234, 9876)
    AddItemToList("devflt1", item1)
    AddItemToList("devflt2", item2)

    filteredList = []

    # Filter by vendor+product
    CreateFilteredList(filteredList, 1234, 5678)
    assert len(filteredList) == 1
    filteredList.clear()

    # Filter by vendor only
    CreateFilteredList(filteredList, 1234, 0)
    assert len(filteredList) == 2
    filteredList.clear()

    # Filter by no filter (should return all)
    CreateFilteredList(filteredList, 0, 0)
    assert len(filteredList) >= 2