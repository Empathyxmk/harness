package info.debatty.java.stringsimilarity;

import org.junit.Test;
import static org.junit.Assert.*;

public class MetricLCSPublicTest {

    @Test
    public void testDistance() {
        MetricLCS metric = new MetricLCS();
        assertEquals(1.0, metric.distance("XYZA", "XYZZ"), 0.001);
        assertEquals(2.0, metric.distance("testcase", "castes"), 0.001);
        assertEquals(3.0, metric.distance("LCS", "CSL"), 0.001);
        assertEquals(0.0, metric.distance("public", "public"), 0.001);
    }

    @Test
    public void testSimilarity() {
        MetricLCS metric = new MetricLCS();
        assertEquals(0.75, metric.similarity("XYZA", "XYZZ"), 0.001);
        assertEquals(0.5, metric.similarity("testcase", "castes"), 0.01);
        assertEquals(0.5, metric.similarity("LCS", "CSL"), 0.001);
    }

    @Test
    public void testNullAndEmpty() {
        MetricLCS metric = new MetricLCS();
        assertEquals(1.0, metric.similarity("", ""), 1e-9);
        assertEquals(0.0, metric.similarity("", "foo"), 1e-9);
        assertEquals(0.0, metric.similarity("foo", ""), 1e-9);
    }
}