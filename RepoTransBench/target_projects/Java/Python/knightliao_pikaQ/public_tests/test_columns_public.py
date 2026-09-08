def test_name_constant_not_null():
    class Columns:
        NAME = "name"
        CAMPAIGN_ID = "campaignId"
    assert Columns.NAME is not None
    assert len(Columns.NAME) > 2

def test_campaign_id_constant_has_id():
    class Columns:
        NAME = "name"
        CAMPAIGN_ID = "campaignId"
    assert Columns.CAMPAIGN_ID.endswith("Id")