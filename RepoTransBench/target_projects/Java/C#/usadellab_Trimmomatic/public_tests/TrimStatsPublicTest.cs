using System;
using Xunit;
using UsadellabTrimmomatic;
using UsadellabTrimmomatic.fastq;
using System.IO;

namespace UsadellabTrimmomatic.PublicTests
{
    public class TrimStatsPublicTest
    {
        [Fact]
        public void TestMergeEffect()
        {
            var stats1 = new TrimStats();
            var stats2 = new TrimStats();
            var rec = new FastqRecord("other", "xyz", "===!");
            var orig = new FastqRecord[] { rec };
            var surv = new FastqRecord[] { rec };
            stats2.LogPair(orig, surv);
            stats1.Merge(stats2);
            Assert.NotNull(stats1);
        }

        [Fact]
        public void TestLogPairDropAndSurvive()
        {
            var stats = new TrimStats();
            var recDrop = new FastqRecord("d", "ggg", "!!!");
            var recSurvive = new FastqRecord("s", "ccc", "$$$");
            var orig = new FastqRecord[] { recDrop };
            var surv = new FastqRecord[] { null };
            stats.LogPair(orig, surv); // drop
            var orig2 = new FastqRecord[] { recSurvive };
            var surv2 = new FastqRecord[] { recSurvive };
            stats.LogPair(orig2, surv2); // survives

            var origPair = new FastqRecord[] { recDrop, recSurvive };
            var survPair = new FastqRecord[] { recSurvive, null };
            stats.LogPair(origPair, survPair); // only left survived
        }

        [Fact]
        public void TestProcessStatsSEAndPEDistinct()
        {
            var stats = new TrimStats();
            var rec = new FastqRecord("n2", "AGAG", "zzzx");
            stats.LogPair(new FastqRecord[] { rec }, new FastqRecord[] { null });
            var se = stats.ProcessStatsSE(null);
            Assert.Contains("input reads", se.ToLower());
            var pe = stats.ProcessStatsPE(null);
            Assert.Contains("input read pairs", pe.ToLower());
        }

        [Fact]
        public void TestProcessStatsPEWithCustomFile()
        {
            var stats = new TrimStats();
            var tmp = Path.GetTempFileName();
            var file = new FileInfo(tmp);
            var rec = new FastqRecord("r3", "ATGCT", "####.");
            stats.LogPair(new FastqRecord[] { rec }, new FastqRecord[] { null });
            stats.ProcessStatsPE(file);
            Assert.True(File.Exists(tmp));
            File.Delete(tmp);
        }
    }
}