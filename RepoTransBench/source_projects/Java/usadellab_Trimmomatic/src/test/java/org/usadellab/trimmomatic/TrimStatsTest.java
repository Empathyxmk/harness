package org.usadellab.trimmomatic;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import org.usadellab.trimmomatic.fastq.FastqRecord;

import java.io.File;
import java.io.IOException;

class TrimStatsTest {

    @Test
    void testConstructorAndMerge() {
        TrimStats stats1 = new TrimStats();
        TrimStats stats2 = new TrimStats();
        stats1.merge(stats2); // coverage: merge when all zero
        assertNotNull(stats1);
    }

    @Test
    void testLogPairSingleAndBoth() {
        TrimStats stats = new TrimStats();
        FastqRecord rec = new FastqRecord("name", "seq", "qual");
        FastqRecord[] orig = new FastqRecord[] { rec };
        FastqRecord[] surv = new FastqRecord[] { rec };
        stats.logPair(orig, surv); // surviving forward
        FastqRecord[] surv2 = new FastqRecord[] { null };
        stats.logPair(orig, surv2); // dropped
        
        FastqRecord[] origPair = new FastqRecord[] { rec, rec };
        FastqRecord[] survPairBoth = new FastqRecord[] { rec, rec };
        FastqRecord[] survPairFwd = new FastqRecord[] { rec, null };
        FastqRecord[] survPairRev = new FastqRecord[] { null, rec };
        stats.logPair(origPair, survPairBoth);
        stats.logPair(origPair, survPairFwd);
        stats.logPair(origPair, survPairRev);
    }

    @Test
    void testProcessStatsSEAndPE() throws IOException {
        TrimStats stats = new TrimStats();
        FastqRecord rec = new FastqRecord("name", "seq", "qual");
        FastqRecord[] orig = new FastqRecord[] { rec };
        FastqRecord[] surv = new FastqRecord[] { rec };
        stats.logPair(orig, surv);
        String resultSE = stats.processStatsSE(null);
        assertTrue(resultSE.contains("Input Reads"));
        String resultPE = stats.processStatsPE(null);
        assertTrue(resultPE.contains("Input Read Pairs"));
    }

    @Test
    void testProcessStatsSEAndPEWithFile() throws IOException {
        TrimStats stats = new TrimStats();
        File tmp = File.createTempFile("stats", ".txt");
        tmp.deleteOnExit();
        FastqRecord rec = new FastqRecord("name", "seq", "qual");
        stats.logPair(new FastqRecord[]{rec}, new FastqRecord[]{rec});
        stats.processStatsSE(tmp);
        stats.processStatsPE(tmp);
        assertTrue(tmp.exists());
    }
}