import unittest
import sys
import types

import importlib
from unittest.mock import MagicMock, patch

# Patch imports for plugin sample
sys.modules['deye_plugin_loader'] = types.SimpleNamespace(DeyePluginContext=object)
sys.modules['deye_events'] = types.SimpleNamespace(
    DeyeEventProcessor=object, DeyeEventList=object, DeyeObservationEvent=object
)

# Now import the plugin (after mocking dependencies)
import plugins.deye_plugin_sample as deye_plugin_sample


class DummySensor:
    def __init__(self, mqtt_topic_suffix):
        self.mqtt_topic_suffix = mqtt_topic_suffix


class DummyObservation:
    def __init__(self, sensor, value):
        self.sensor = sensor
        self.value = value


class DummyObservationEvent:
    def __init__(self, sensor_suffix, value):
        self.observation = DummyObservation(DummySensor(sensor_suffix), value)


class DummyDeyeEventList(list):
    def __init__(self, logger_index, *events):
        super().__init__(events)
        self.logger_index = logger_index


class PluginsDeyePluginSampleTest(unittest.TestCase):
    def test_get_id(self):
        publisher = deye_plugin_sample.DeyeSamplePublisher()
        self.assertEqual(publisher.get_id(), "sample_publisher")

    def test_plugin_init_get_processors(self):
        ctx = object()
        plugin = deye_plugin_sample.DeyePlugin(ctx)
        processors = plugin.get_event_processors()
        self.assertEqual(len(processors), 1)
        self.assertIsInstance(processors[0], deye_plugin_sample.DeyeSamplePublisher)

    def test_process_with_observation_event(self):
        publisher = deye_plugin_sample.DeyeSamplePublisher()
        # Patch isinstance to always return True for DeyeObservationEvent
        with patch('plugins.deye_plugin_sample.DeyeObservationEvent', DummyObservationEvent):
            with patch('builtins.print') as mock_print:
                event = DummyObservationEvent("mysensor", 42)
                events = DummyDeyeEventList(3, event)
                publisher.process(events)
                # Should print logger_index and the event value
                self.assertTrue(any("mysensor" in str(args[0]) for args, _ in mock_print.call_args_list))


if __name__ == "__main__":
    unittest.main()