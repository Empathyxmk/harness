using System;
using System.Collections.Generic;
using System.IO;
using Xunit;
using UsadellabTrimmomatic;
using UsadellabTrimmomatic.fastq;

namespace UsadellabTrimmomatic.PublicTests
{
    public class DummyPublicFastqRecord : FastqRecord
    {
        public DummyPublicFastqRecord(string n) : base(n, "TGCA", "@@@@") { }
    }

    public class PairomaticPublicTest
    {
        private FileInfo CreateTempFastq(List<string> names, char? delimiter)
        {
            var tempFile = new FileInfo(Path.GetTempFileName());
            using (var w = new StreamWriter(tempFile.FullName, false))
            {
                foreach (var n in names)
                {
                    w.WriteLine("@" + n + (delimiter == null ? "" : delimiter + "2"));
                    w.WriteLine("TGCA");
                    w.WriteLine("+");
                    w.WriteLine("@@@@");
                }
            }
            return tempFile;
        }

        [Fact]
        public void TestGetFastqNamesDelimiterDash()
        {
            var p = new Pairomatic();
            var names = new List<string> { "QX", "ZE" };
            var f = CreateTempFastq(names, '-');
            var result = InvokeGetFastqNames(p, f, '-');
            Assert.Equal(2, result.Count);
            File.Delete(f.FullName);
        }

        [Fact]
        public void TestGetFastqNamesNoDelimiterMultiple()
        {
            var p = new Pairomatic();
            var names = new List<string> { "A010", "B020" };
            var f = CreateTempFastq(names, null);
            var result = InvokeGetFastqNames(p, f, null);
            Assert.Equal(2, result.Count);
            File.Delete(f.FullName);
        }

        [Fact]
        public void TestGetFastqNamesFailOnDelimiter()
        {
            var p = new Pairomatic();
            var names = new List<string> { "NM" };
            var f = CreateTempFastq(names, null);
            var ex = Assert.Throws<Exception>(() => {
                InvokeGetFastqNames(p, f, '-');
            });
            Assert.Contains("Failed to find expected delimiter", ex.Message);
            File.Delete(f.FullName);
        }

        [Fact]
        public void TestEqualOrderingMismatch()
        {
            var p = new Pairomatic();
            var s1 = new LinkedHashSet<string>(new[] { "U", "V" });
            var s2 = new LinkedHashSet<string>(new[] { "V", "U" });
            Assert.False(InvokeEqualOrdering(p, s1, s2));
            var s3 = new LinkedHashSet<string>(new[] { "U", "V" });
            Assert.True(InvokeEqualOrdering(p, s1, s3));
        }

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