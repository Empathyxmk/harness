using System;
using Xunit;
using UsadellabTrimmomatic;
using UsadellabTrimmomatic.fastq;
using System.IO;

namespace UsadellabTrimmomatic.Tests
{
    public class TrimStatsTest
    {
        [Fact]
        public void TestConstructorAndMerge()
        {
            var stats1 = new TrimStats();
            var stats2 = new TrimStats();
            stats1.Merge(stats2); // coverage: merge when all zero
            Assert.NotNull(stats1);
        }

        [Fact]
        public void TestLogPairSingleAndBoth()
        {
            var stats = new TrimStats();
            var rec = new FastqRecord("name", "seq", "qual");
            var orig = new FastqRecord[] { rec };
            var surv = new FastqRecord[] { rec };
            stats.LogPair(orig, surv); // surviving forward
            var surv2 = new FastqRecord[] { null };
            stats.LogPair(orig, surv2); // dropped

            var origPair = new FastqRecord[] { rec, rec };
            var survPairBoth = new FastqRecord[] { rec, rec };
            var survPairFwd = new FastqRecord[] { rec, null };
            var survPairRev = new FastqRecord[] { null, rec };
            stats.LogPair(origPair, survPairBoth);
            stats.LogPair(origPair, survPairFwd);
            stats.LogPair(origPair, survPairRev);
        }

        [Fact]
        public void TestProcessStatsSEAndPE()
        {
            var stats = new TrimStats();
            var rec = new FastqRecord("name", "seq", "qual");
            var orig = new FastqRecord[] { rec };
            var surv = new FastqRecord[] { rec };
            stats.LogPair(orig, surv);
            var resultSE = stats.ProcessStatsSE(null);
            Assert.Contains("Input Reads", resultSE);
            var resultPE = stats.ProcessStatsPE(null);
            Assert.Contains("Input Read Pairs", resultPE);
        }

        [Fact]
        public void TestProcessStatsSEAndPEWithFile()
        {
            var stats = new TrimStats();
            var tmp = Path.GetTempFileName();
            var file = new FileInfo(tmp);
            var rec = new FastqRecord("name", "seq", "qual");
            stats.LogPair(new FastqRecord[] { rec }, new FastqRecord[] { rec });
            stats.ProcessStatsSE(file);
            stats.ProcessStatsPE(file);
            Assert.True(File.Exists(tmp));
            File.Delete(tmp); // cleanup
        }
    }
}