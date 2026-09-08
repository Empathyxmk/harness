import pytest

class RocketMQMessageListenerBeanPostProcessor:
    def postProcessAfterInitialization(self, bean, name):
        # Simulate: returns the bean if it's not a listener
        return bean

def test_supports_bean_with_public_data():
    processor = RocketMQMessageListenerBeanPostProcessor()
    class MockBean:
        def listenPublic(self, message):
            pass
    mockBean = MockBean()
    processed = processor.postProcessAfterInitialization(mockBean, "someOtherBean")
    # Should NOT transform the bean to a RocketMQMessageListener (no annotation system in Python)
    assert not isinstance(processed, type(lambda: None))