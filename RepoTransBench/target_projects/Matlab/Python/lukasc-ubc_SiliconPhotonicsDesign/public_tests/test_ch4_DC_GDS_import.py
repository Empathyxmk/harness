def dummy_gds_id_public(input_str):
    return input_str

def test_gds_id_public():
    id_str = dummy_gds_id_public('GDS123')
    assert id_str == 'GDS123'

def test_gds_empty_public():
    id_str = dummy_gds_id_public('')
    assert id_str == ''