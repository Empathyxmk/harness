import unittest
from datetime import datetime
from src.deye_events import DeyeObservationEvent, DeyeEventList
from src.deye_observation import Observation


class DummySensor:
    pass

class TestDeyeEventsPublic(unittest.TestCase):

    def test_event_list_length_and_iteration(self):
        e1 = DeyeObservationEvent(Observation(DummySensor(), datetime.now(), 1.1))
        e2 = DeyeObservationEvent(Observation(DummySensor(), datetime.now(), 3.3))
        events = DeyeEventList([e1, e2])
        self.assertEqual(len(events), 2)
        self.assertListEqual([e for e in events], [e1, e2])

    def test_event_list_append_and_getitem(self):
        e1 = DeyeObservationEvent(Observation(DummySensor(), datetime.now(), 4.4))
        l = DeyeEventList()
        l.append(e1)
        self.assertEqual(l[0], e1)
        self.assertEqual(len(l), 1)

    def test_event_list_repr(self):
        e1 = DeyeObservationEvent(Observation(DummySensor(), datetime.now(), 57.6))
        l = DeyeEventList([e1])
        r = repr(l)
        self.assertIn("DeyeEventList", r)
        self.assertIn("DeyeObservationEvent", r)


if __name__ == "__main__":
    unittest.main()