import unittest
import time
from datetime import datetime, timedelta

class JTimeTransform:
    # Python stub for testing
    def __init__(self, *args):
        if not args:
            dt = datetime.now()
            self._dt = dt
        elif len(args) == 1:
            timestamp = args[0]
            self._dt = datetime.fromtimestamp(timestamp)
        elif len(args) == 3:
            # Java months are 0-based but Python's are 1-based, adjust accordingly
            y, m, d = args
            # The Java tests seem to expect 0-based months as "Mar" is implemented as 2 (i.e., March)
            self._dt = datetime(y, m + 1, d)
        else:
            raise ValueError("unexpected constructor arguments")
    def getYear(self):
        return self._dt.year
    def getMonth(self):
        return self._dt.month
    def getDay(self):
        return self._dt.day
    def getTimestamp(self):
        return int(self._dt.timestamp())
    def toString(self, fmt_or_recent):
        if isinstance(fmt_or_recent, JTimeTransform.RecentDateFormat):
            return fmt_or_recent.format(self, 0)
        else:
            # fmt_or_recent is a string
            return self._dt.strftime(fmt_or_recent)
    def parse(self, fmt, date_str):
        try:
            dt = datetime.strptime(date_str, fmt)
            ret = JTimeTransform()
            ret._dt = dt
            return ret
        except Exception:
            return None

    class RecentDateFormat:
        # Very rough mock of the date format logic
        def __init__(self, fmt):
            self.fmt = fmt
        def format(self, jtt, delta):
            if abs(delta) < 60:
                if delta >= 0:
                    return f"{abs(delta)}秒前"
                else:
                    return f"{abs(delta)}秒后"
            elif abs(delta) < 3600:
                if delta >= 0:
                    return f"{abs(delta//60)}分钟前"
                else:
                    return f"{abs(delta//60)}分钟后"
            elif abs(delta) < 86400:
                if delta >= 0:
                    return f"{abs(delta//3600)}小时前"
                else:
                    return f"{abs(delta//3600)}小时后"
            elif abs(delta) < 604800:
                if delta >= 0:
                    return f"{abs(delta//86400)}天前"
                else:
                    return f"{abs(delta//86400)}天后"
            else:
                return jtt._dt.strftime(self.fmt)

class TestJTimeTransform(unittest.TestCase):
    def testDefaultConstructor(self):
        jtt = JTimeTransform()
        self.assertIsNotNone(jtt)
        self.assertTrue(jtt.getYear() > 2000)
        self.assertTrue(jtt.getMonth() > 0 and jtt.getMonth() < 13)
        self.assertTrue(jtt.getDay() > 0 and jtt.getDay() < 32)
        self.assertTrue(jtt.getTimestamp() > 0)

    def testLongConstructor(self):
        now = int(time.time())
        jtt = JTimeTransform(now)
        self.assertAlmostEqual(now, jtt.getTimestamp(), delta=1)

    def testYMDConstructor(self):
        jtt = JTimeTransform(2023, 2, 25) # Mar 25, 2023
        self.assertEqual(2023, jtt.getYear())
        self.assertEqual(3, jtt.getMonth())
        self.assertEqual(25, jtt.getDay())

    def testToStringFormat(self):
        jtt = JTimeTransform(2022, 0, 2) # Jan 2, 2022
        s = jtt.toString("%Y-%m-%d")
        self.assertTrue(s.startswith("2022-01-02"))

    def testParseSuccess(self):
        jtt = JTimeTransform(2022, 11, 20)
        result = jtt.parse("%Y-%m-%d", "2022-12-25")
        self.assertIsNotNone(result)
        self.assertEqual(2022, result.getYear())
        self.assertEqual(12, result.getMonth())
        self.assertEqual(25, result.getDay())

    def testParseFailure(self):
        jtt = JTimeTransform(2022, 11, 20)
        result = jtt.parse("%Y-%m-%d", "abc")
        self.assertIsNone(result)

    def testRecentDateFormat(self):
        now = int(time.time())
        just_now = JTimeTransform(now)
        one_min_ago = JTimeTransform(now - 60)
        one_hour_ago = JTimeTransform(now - 3600)
        yesterday = JTimeTransform(now - 86400)
        tomorrow = JTimeTransform(now + 86400)

        rdf = JTimeTransform.RecentDateFormat("%Y-%m-%d")
        sec_text = rdf.format(JTimeTransform(now-1), 1)
        self.assertTrue("秒前" in sec_text or "秒" in sec_text)

        min_text = rdf.format(one_min_ago, 60*1)
        self.assertTrue("分钟前" in min_text)

        hour_text = rdf.format(one_hour_ago, 3600)
        self.assertTrue("小时前" in hour_text)

        dt_text = one_min_ago.toString(rdf)
        self.assertIsNotNone(dt_text)

        future_sec = rdf.format(JTimeTransform(now+1), -1)
        self.assertTrue("秒后" in future_sec or "秒" in future_sec)
        future_min = rdf.format(JTimeTransform(now+80), -80)
        self.assertTrue("分钟后" in future_min)
        fallback_past = rdf.format(yesterday, 86400)
        self.assertIsNotNone(fallback_past)
        fallback_future = rdf.format(tomorrow, -86400)
        self.assertIsNotNone(fallback_future)

if __name__ == "__main__":
    unittest.main()