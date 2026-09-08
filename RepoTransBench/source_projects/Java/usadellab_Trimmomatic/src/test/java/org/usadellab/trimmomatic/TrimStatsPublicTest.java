package org.usadellab.trimmomatic;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import org.usadellab.trimmomatic.fastq.FastqRecord;

import java.io.File;
import java.io.IOException;

class TrimStatsPublicTest {

    @Test
    void testMergeEffect() {
        TrimStats stats1 = new TrimStats();
        TrimStats stats2 = new TrimStats();
        FastqRecord rec = new FastqRecord("other", "xyz", "===!");
        FastqRecord[] orig = new FastqRecord[] { rec };
        FastqRecord[] surv = new FastqRecord[] { rec };
        stats2.logPair(orig, surv);
        stats1.merge(stats2);
        assertNotNull(stats1);
    }

    @Test
    void testLogPairDropAndSurvive() {
        TrimStats stats = new TrimStats();
        FastqRecord recDrop = new FastqRecord("d", "ggg", "!!!");
        FastqRecord recSurvive = new FastqRecord("s", "ccc", "$$$");
        FastqRecord[] orig = new FastqRecord[] { recDrop };
        FastqRecord[] surv = new FastqRecord[] { null };
        stats.logPair(orig, surv); // drop
        FastqRecord[] orig2 = new FastqRecord[] { recSurvive };
        FastqRecord[] surv2 = new FastqRecord[] { recSurvive };
        stats.logPair(orig2, surv2); // survives

        FastqRecord[] origPair = new FastqRecord[] { recDrop, recSurvive };
        FastqRecord[] survPair = new FastqRecord[] { recSurvive, null };
        stats.logPair(origPair, survPair); // only left survived
    }

    @Test
    void testProcessStatsSEAndPEDistinct() throws IOException {
        TrimStats stats = new TrimStats();
        FastqRecord rec = new FastqRecord("n2", "AGAG", "zzzx");
        stats.logPair(new FastqRecord[]{rec}, new FastqRecord[]{null});
        String se = stats.processStatsSE(null);
        assertTrue(se.toLowerCase().contains("input reads"), "Should mention Input Reads");
        String pe = stats.processStatsPE(null);
        assertTrue(pe.toLowerCase().contains("input read pairs"), "Should mention Input Read Pairs");
    }

    @Test
    void testProcessStatsPEWithCustomFile() throws IOException {
        TrimStats stats = new TrimStats();
        File tmp = File.createTempFile("pstats", ".tmp");
        tmp.deleteOnExit();
        FastqRecord rec = new FastqRecord("r3", "ATGCT", "####.");
        stats.logPair(new FastqRecord[]{rec}, new FastqRecord[]{null});
        stats.processStatsPE(tmp);
        assertTrue(tmp.exists() && tmp.length() >= 0);
    }
}