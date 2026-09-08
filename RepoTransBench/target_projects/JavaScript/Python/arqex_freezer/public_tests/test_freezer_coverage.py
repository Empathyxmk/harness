from src.freezer import Freezer

def test_initialize_and_get_correct_tojs():
    f = Freezer({'z': 5, 'w': [7, 8]})
    obj = f.get()
    assert obj['z'] == 5
    assert obj['w'][1] == 8
    assert obj.toJS() == {'z': 5, 'w': [7, 8]}

def test_set_and_update_data_correctly():
    f = Freezer({'p': 1})
    obj = f.get()
    obj.set({'q': 2})
    assert obj['q'] == 2
    assert obj.get('p', None) is None

def test_add_nodes_and_push_correctly_public_data():
    f = Freezer([{'val': 100}])
    arr = f.get()
    arr.push({'val': 200})
    assert len(arr) == 2
    assert arr[1]['val'] == 200

def test_reset_and_replace_data_public():
    f = Freezer({'original': 10})
    obj = f.get()
    f.set({'replaced': "yes"})
    obj2 = f.get()
    assert obj2.get('original', None) is None
    assert obj2['replaced'] == "yes"

def test_emit_update_events_public():
    f = Freezer({'change': 25})
    updated = [False]
    def handler():
        updated[0] = True
        assert updated[0] is True
    f.get().on('update', handler)
    f.get().set({'change': 26})
    assert updated[0] is True