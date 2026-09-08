import pytest
from unittest.mock import Mock

class DexEntry:
    def __init__(self, name):
        self._dex_name = name
    def getDexName(self):
        return self._dex_name

class DexContainer:
    def __init__(self, multi_dex_container, options):
        self.multi_dex_container = multi_dex_container
        self.options = options
    def getEntries(self, preferred=None):
        # Simulate the getEntries logic based on preferred
        all_entries = list(self.multi_dex_container.getDexEntryNames())
        preferred_entries = [e for e in preferred if e in all_entries]
        non_preferred_entries = [e for e in all_entries if e not in preferred_entries]
        ordered = preferred_entries + non_preferred_entries
        return [DexEntry(e) for e in ordered]

class DexOptions:
    def __init__(self):
        self.rootDexOnly = False

def test_dex_entry_order_public():
    INPUT = [
        "main.dex", "data.dex", "core.dex",
        "primary.dex", "secondary.dex", "support.dex"
    ]
    PREFERRED = [
        "core.dex", "main.dex", "support.dex"
    ]
    EXPECTED = [
        "core.dex", "main.dex", "support.dex",
        "data.dex", "primary.dex", "secondary.dex"
    ]
    multi_dex_container = Mock()
    multi_dex_container.getDexEntryNames.return_value = INPUT
    options = DexOptions()
    options.rootDexOnly = True
    container = DexContainer(multi_dex_container, options)
    entries = container.getEntries(PREFERRED)
    entry_names = [e.getDexName() for e in entries]
    assert entry_names == EXPECTED
    multi_dex_container.getDexEntryNames.assert_called_once()
    multi_dex_container.method_calls.count(("getDexEntryNames", (), {})) == 1