def test_campaign_mgr_impl_instance_not_null():
    class CampaignMgrImpl:
        pass
    mgr = CampaignMgrImpl()
    assert mgr is not None