import unittest
import time
from datetime import datetime, timedelta

class JTimeTransform:
    def __init__(self, *args):
        if not args:
            dt = datetime.now()
            self._dt = dt
        elif len(args) == 1:
            timestamp = args[0]
            self._dt = datetime.fromtimestamp(timestamp)
        elif len(args) == 3:
            y, m, d = args
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

class TestJTimeTransformPublic(unittest.TestCase):
    def testDefaultConstructorPublic(self):
        jtt = JTimeTransform()
        self.assertIsNotNone(jtt)
        self.assertTrue(2010 < jtt.getYear() < 2100)
        self.assertTrue(1 <= jtt.getMonth() <= 12)
        self.assertTrue(1 <= jtt.getDay() <= 31)
        self.assertTrue(jtt.getTimestamp() > 0)

    def testLongConstructorPublic(self):
        five_days_ago = int(time.time()) - 432000
        jtt = JTimeTransform(five_days_ago)
        self.assertAlmostEqual(five_days_ago, jtt.getTimestamp(), delta=2)

    def testYMDConstructorPublic(self):
        jtt = JTimeTransform(2021, 10, 11) # Nov 11, 2021
        self.assertEqual(2021, jtt.getYear())
        self.assertEqual(11, jtt.getMonth())
        self.assertEqual(11, jtt.getDay())

    def testToStringFormatPublic(self):
        jtt = JTimeTransform(2020, 6, 4) # July 4, 2020
        s = jtt.toString("%Y/%m/%d")
        self.assertTrue(s.startswith("2020/07/04"))

    def testParseSuccessPublic(self):
        jtt = JTimeTransform(2019, 4, 15)
        result = jtt.parse("%Y/%m/%d", "2019/06/01")
        self.assertIsNotNone(result)
        self.assertEqual(2019, result.getYear())
        self.assertEqual(6, result.getMonth())
        self.assertEqual(1, result.getDay())

    def testParseFailurePublic(self):
        jtt = JTimeTransform(2018, 1, 5)
        result = jtt.parse("%Y/%m/%d", "notadate")
        self.assertIsNone(result)

    def testRecentDateFormatPublic(self):
        now = int(time.time())
        just_now = JTimeTransform(now)
        two_min_ago = JTimeTransform(now - 120)
        three_hour_ago = JTimeTransform(now - 3 * 3600)
        two_days_ago = JTimeTransform(now - 2 * 86400)
        two_days_later = JTimeTransform(now + 2 * 86400)

        rdf = JTimeTransform.RecentDateFormat("%Y/%m/%d")
        sec_text = rdf.format(JTimeTransform(now-2), 2)
        self.assertTrue("秒前" in sec_text or "秒" in sec_text)
        min_text = rdf.format(two_min_ago, 120)
        self.assertTrue("分钟前" in min_text)
        hour_text = rdf.format(three_hour_ago, 3 * 3600)
        self.assertTrue("小时前" in hour_text)
        dt_text = two_min_ago.toString(rdf)
        self.assertIsNotNone(dt_text)
        future_sec = rdf.format(JTimeTransform(now+3), -3)
        self.assertTrue("秒后" in future_sec or "秒" in future_sec)
        future_day = rdf.format(JTimeTransform(now+3600*50), -3600*50)
        self.assertTrue("天后" in future_day or "天" in future_day)
        fallback_past = rdf.format(two_days_ago, 2 * 86400)
        self.assertIsNotNone(fallback_past)
        fallback_future = rdf.format(two_days_later, -2 * 86400)
        self.assertIsNotNone(fallback_future)

if __name__ == "__main__":
    unittest.main()