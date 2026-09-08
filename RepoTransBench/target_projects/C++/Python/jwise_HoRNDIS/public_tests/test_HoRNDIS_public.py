import pytest

class IOEthernetController:
    # Minimal stub, as in original test
    pass

class IOEthernetInterface:
    # Minimal stub, as in original test
    pass

def test_public_compile_sanity():
    """
    Public test: Variation of the basic sanity test for HoRNDIS coverage bring-up.

    Equivalent to:
    IOEthernetController controller_array[2];
    IOEthernetInterface interface_array[2];
    (void)controller_array;
    (void)interface_array;
    SUCCEED();
    """
    controller_array = [IOEthernetController(), IOEthernetController()]
    interface_array = [IOEthernetInterface(), IOEthernetInterface()]
    # The C++ test just instantiates; Python should do the same and assert class
    assert all(isinstance(c, IOEthernetController) for c in controller_array)
    assert all(isinstance(i, IOEthernetInterface) for i in interface_array)