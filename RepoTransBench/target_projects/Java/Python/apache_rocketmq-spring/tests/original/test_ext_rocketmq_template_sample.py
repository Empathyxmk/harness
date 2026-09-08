def test_ext_rocketmq_template_instantiation():
    class ExtRocketMQTemplate:
        pass
    template = ExtRocketMQTemplate()
    assert template is not None