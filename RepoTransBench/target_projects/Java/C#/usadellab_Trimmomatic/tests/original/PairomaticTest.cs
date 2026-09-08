using System;
using Xunit;
using System.Collections.Generic;
using System.IO;
using UsadellabTrimmomatic;
using UsadellabTrimmomatic.fastq;

namespace UsadellabTrimmomatic.Tests
{
    public class DummyFastqRecord : FastqRecord
    {
        public DummyFastqRecord(string n) : base(n, "ACGT", "!!!") { }
    }

    public class PairomaticTest
    {
        // Create a temporary fastq file for the test
        private FileInfo CreateFastqFile(List<string> names, char? delimiter)
        {
            var tempFile = new FileInfo(Path.GetTempFileName());
            using (var w = new StreamWriter(tempFile.FullName, false))
            {
                foreach (var n in names)
                {
                    w.WriteLine("@" + n + (delimiter == null ? "" : delimiter + "1"));
                    w.WriteLine("ACGT");
                    w.WriteLine("+");
                    w.WriteLine("!!!!");
                }
            }
            return tempFile;
        }

        [Fact]
        public void TestGetFastqNamesNoDelimiter()
        {
            var p = new Pairomatic();
            var names = new List<string> { "x1", "y2" };
            var f = CreateFastqFile(names, null);
            var result = InvokeGetFastqNames(p, f, null);
            Assert.Equal(2, result.Count);
            File.Delete(f.FullName);
        }

        [Fact]
        public void TestGetFastqNamesWithDelimiter()
        {
            var p = new Pairomatic();
            var names = new List<string> { "A", "B" };
            var f = CreateFastqFile(names, ':');
            var result = InvokeGetFastqNames(p, f, ':');
            Assert.Equal(2, result.Count);
            File.Delete(f.FullName);
        }

        [Fact]
        public void TestGetFastqNamesDelimiterNotFound()
        {
            var p = new Pairomatic();
            var names = new List<string> { "Z" };
            var f = CreateFastqFile(names, null);
            var ex = Assert.Throws<Exception>(() => {
                InvokeGetFastqNames(p, f, ':');
            });
            Assert.Contains("Failed to find expected delimiter", ex.Message);
            File.Delete(f.FullName);
        }

        [Fact]
        public void TestEqualOrdering()
        {
            var p = new Pairomatic();
            var s1 = new LinkedHashSet<string>(new[] { "A", "B" });
            var s2 = new LinkedHashSet<string>(new[] { "A", "B" });
            Assert.True(InvokeEqualOrdering(p, s1, s2));
            var s3 = new LinkedHashSet<string>(new[] { "B", "A" });
            Assert.False(InvokeEqualOrdering(p, s1, s3));
        }

        // Reflection for private methods
        private ISet<string> InvokeGetFastqNames(Pairomatic p, FileInfo f, char? d)
        {
            var method = typeof(Pairomatic).GetMethod("GetFastqNames", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
            return (ISet<string>)method.Invoke(p, new object[] { f, d });
        }

        private bool InvokeEqualOrdering(Pairomatic p, ISet<string> s1, ISet<string> s2)
        {
            var method = typeof(Pairomatic).GetMethod("EqualOrdering", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
            return (bool)method.Invoke(p, new object[] { s1, s2 });
        }
    }

    // Simple implementation of LinkedHashSet for ordered set behavior
    public class LinkedHashSet<T> : HashSet<T>
    {
        private readonly List<T> _order = new List<T>();
        public LinkedHashSet(IEnumerable<T> items = null) : base()
        {
            if (items != null)
            {
                foreach (var item in items)
                    Add(item);
            }
        }
        public new bool Add(T item)
        {
            if (!base.Add(item))
                return false;
            _order.Add(item);
            return true;
        }
        public new IEnumerator<T> GetEnumerator() => _order.GetEnumerator();
    }
}