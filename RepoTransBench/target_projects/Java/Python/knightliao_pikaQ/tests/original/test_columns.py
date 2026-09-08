def test_name_constant():
    class Columns:
        NAME = "name"
        CAMPAIGN_ID = "campaignId"
    assert Columns.NAME == "name"

def test_campaign_id_constant():
    class Columns:
        NAME = "name"
        CAMPAIGN_ID = "campaignId"
    assert Columns.CAMPAIGN_ID == "campaignId"