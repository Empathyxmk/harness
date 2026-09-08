def test_default_lifecycle_behavior_public():
    class DefaultRocketMQListenerContainer:
        def __init__(self):
            self._running = False
            self._name = None
        def setName(self, name):
            self._name = name
        def isRunning(self):
            return self._running
    container = DefaultRocketMQListenerContainer()
    container.setName("publicContainer")
    assert not container.isRunning()