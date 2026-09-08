import ast
import logging
import time
import unittest
import six

from plop.collector import Collector, PlopFormatter

class PublicCollectorTest(unittest.TestCase):
    def filter_stacks(self, collector):
        stack_counts = ast.literal_eval(PlopFormatter().format(collector))
        counts = {}
        for stack, count in six.iteritems(stack_counts):
            filtered_stack = [frame[2] for frame in stack
                              if frame[0].endswith('test_public_collector.py')]
            if filtered_stack:
                counts[tuple(filtered_stack)] = count
        return counts

    def check_counts(self, counts, expected):
        failed = False
        output = []
        for stack, count in six.iteritems(expected):
            self.assertTrue(stack in counts)
            ratio = float(counts[stack]) / float(count)
            output.append("%s: expected %s, got %s (%s)" %
                          (stack, count, counts[stack], ratio))
            if not (0.01 <= ratio <= 3):
                failed = True
        if failed:
            for line in output:
                logging.warning(line)
            for key in set(counts.keys()) - set(expected.keys()):
                logging.warning('unexpected key: %s: got %s' % (key, counts[key]))
            self.fail("collected data did not meet expectations")

    def test_collector(self):
        start = time.time()
        def x(end):
            while time.time() < end: pass
            z(time.time() + 0.08)
        def y(end):
            while time.time() < end: pass
            z(time.time() + 0.05)
        def z(end):
            while time.time() < end: pass
        collector = Collector(interval=0.012, mode='prof')
        collector.start()
        x(time.time() + 0.09)
        y(time.time() + 0.13)
        z(time.time() + 0.11)
        end = time.time()
        collector.stop()
        elapsed = end - start
        self.assertTrue(0.09 < elapsed < 1.5, elapsed)

        counts = self.filter_stacks(collector)
        # Use distinct function name sequences so the test values differ
        expected = {
            ("x", "test_collector"): 7,
            ("z", "x", "test_collector"): 7,
            ("y", "test_collector"): 11,
            ("z", "y", "test_collector"): 5,
            ("z", "test_collector"): 11,
        }
        self.check_counts(counts, expected)
        # test time per sample
        if collector.samples_taken:
            time_per_sample = float(collector.sample_time) / collector.samples_taken
            self.assertTrue(time_per_sample < 0.000300 or time_per_sample > 0.000001, time_per_sample)