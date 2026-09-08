from unittest import mock


def test_different_init_triggers_sync_public():
    syncer = mock.Mock()
    syncer.init()
    syncer.init.assert_called_once()
    syncer.sync([])
    syncer.sync.assert_called_with([])