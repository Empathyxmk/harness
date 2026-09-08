def test_instantiate_auto_config_public():
    class RocketMQAutoConfiguration:
        pass
    config = RocketMQAutoConfiguration()
    assert config is not None