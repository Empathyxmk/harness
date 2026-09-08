package com.github.nexmark.flink.workload;

import org.apache.flink.configuration.Configuration;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class WorkloadSuiteTest {

    @Test
    void testEqualsAndHashCode() {
        WorkloadSuite suite1 = new WorkloadSuite(new HashMap<>());
        WorkloadSuite suite2 = new WorkloadSuite(new HashMap<>());
        assertEquals(suite1, suite2);
        assertEquals(suite1.hashCode(), suite2.hashCode());
    }

    @Test
    void testToString() {
        WorkloadSuite suite = new WorkloadSuite(new HashMap<>());
        assertTrue(suite.toString().contains("query2Workload"));
    }

    @Test
    void testFromConfReturnsSuite() {
        Configuration conf = new Configuration();
        conf.setString("nexmark.workload.suite.s1.queries", "q1");
        conf.setString("nexmark.workload.suite.s1.tps", "1000");
        conf.setString("nexmark.workload.suite.s1.events.num", "10000");
        WorkloadSuite suite = WorkloadSuite.fromConf(conf, "oa");
        assertNotNull(suite);
        assertNotNull(suite.getQueryWorkload("q1"));
    }
}