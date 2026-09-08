import unittest
import sys
import types
from unittest.mock import MagicMock, patch
import datetime

# Provide minimal mocks for deye_events, deye_observation, deye_sensors_aggregated
sys.modules['deye_events'] = types.SimpleNamespace(
    DeyeEventProcessor=object, DeyeEventList=object, DeyeObservationEvent=object
)
sys.modules['deye_observation'] = types.SimpleNamespace(Observation=object)
deye_sensors_aggregated_mock = types.SimpleNamespace(
    aggregated_ac_active_power_sensor=types.SimpleNamespace(mqtt_topic_suffix="ac/power"),
    aggregated_day_energy_sensor=types.SimpleNamespace(mqtt_topic_suffix="day/energy"),
)
sys.modules['deye_sensors_aggregated'] = deye_sensors_aggregated_mock

import src.deye_multi_inverter_data_aggregator as multiagg


class DummyObservation:
    def __init__(self, sensor_topic, value):
        self.sensor = types.SimpleNamespace(mqtt_topic_suffix=sensor_topic)
        self.value = value


class DummyEvent:
    def __init__(self, topic_suffix, value):
        self.observation = DummyObservation(topic_suffix, value)
    # Must pass DeyeObservationEvent isinstance check, so we patch accordingly


class DummyDeyeEventList(list):
    def __init__(self, logger_index, *events):
        super().__init__(events)
        self.logger_index = logger_index


class TestDeyeMultiInverterDataAggregator(unittest.TestCase):
    def setUp(self):
        self.aggregator = multiagg.DeyeMultiInverterDataAggregator()

    def test_get_id_and_description(self):
        self.assertEqual(self.aggregator.get_id(), "multi_inverter_data_aggregator")
        self.assertIn("Aggregate metrics", self.aggregator.get_description())

    def test_process_and_aggregate(self):
        # Patch isinstance to allow DummyEvent to be handled as DeyeObservationEvent
        with patch("src.deye_multi_inverter_data_aggregator.DeyeObservationEvent", DummyEvent):
            el = DummyDeyeEventList(1, DummyEvent("ac/power", 123.4), DummyEvent("day/energy", 12.3))
            self.aggregator.process(el)
            # Aggregation: should include our values
            aggs = self.aggregator.aggregate()
            # The return is a list of Observation objects (should be 2 entries, value equals our value)
            self.assertEqual(len(aggs), 2)
            self.assertEqual(aggs[0].value, 123.4)
            self.assertEqual(aggs[1].value, 12.3)

    def test_no_event_type(self):
        # Test gracefully skipping events not DeyeObservationEvent
        with patch("src.deye_multi_inverter_data_aggregator.DeyeObservationEvent", DummyEvent):
            e = DummyDeyeEventList(2)
            # Should not fail
            self.aggregator.process(e)
            aggs = self.aggregator.aggregate()
            self.assertIsNotNone(aggs)

    def test_reset_state(self):
        with patch("src.deye_multi_inverter_data_aggregator.DeyeObservationEvent", DummyEvent):
            el = DummyDeyeEventList(1, DummyEvent("ac/power", 10), DummyEvent("day/energy", 20))
            self.aggregator.process(el)

            # Simulate date change
            self.aggregator._DeyeMultiInverterDataAggregator__last_aggregation_ts = (
                datetime.datetime.now() - datetime.timedelta(days=1)
            )
            aggs = self.aggregator.aggregate()
            self.assertEqual(len(aggs), 2)
            # Now state dicts should be cleared

    def test__get_metric_none(self):
        with patch("src.deye_multi_inverter_data_aggregator.DeyeObservationEvent", DummyEvent):
            el = DummyDeyeEventList(2, DummyEvent("other", 1.23))
            # There is no 'ac/power' or 'day/energy'
            x = self.aggregator._DeyeMultiInverterDataAggregator__get_metric("missing", el)
            self.assertIsNone(x)


if __name__ == "__main__":
    unittest.main()