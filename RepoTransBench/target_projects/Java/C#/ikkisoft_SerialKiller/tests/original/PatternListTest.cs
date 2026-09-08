using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using Xunit;

namespace Ikkisoft.SerialKiller.Tests.Original
{
    public class PatternListTest
    {
        [Fact]
        public void TestCreateNullThrows()
        {
            Assert.Throws<ArgumentNullException>(() => new PatternList((string[])null));
        }

        [Fact]
        public void TestCreateBadPatternThrows()
        {
            Assert.Throws<ArgumentException>(() => new PatternList("("));
        }

        [Fact]
        public void TestCreateEmpty()
        {
            var list = new PatternList();
            var iterator = list.GetEnumerator();
            Assert.False(iterator.MoveNext());
        }

        [Fact]
        public void TestCreateSingle()
        {
            var list = new PatternList("a");
            var iter = list.GetEnumerator();
            Assert.True(iter.MoveNext());
            var pattern = iter.Current;
            Assert.NotNull(pattern);
            Assert.Equal("a", pattern.ToString());
            Assert.False(iter.MoveNext());
        }

        [Fact]
        public void TestCreateSequence()
        {
            var patterns = new[] { "a", "b", "c" };
            var list = new PatternList(patterns);

            int index = 0;
            foreach (var pattern in list)
            {
                Assert.NotNull(pattern);
                Assert.Equal(patterns[index++], pattern.ToString());
            }
            Assert.Equal(3, index);
        }

        [Fact]
        public void TestCreateSafeArgs()
        {
            var patterns = new[] { "1", "2" };
            var list = new PatternList(patterns);
            patterns[1] = "three";

            int index = 0;
            foreach (var pattern in list)
            {
                Assert.Equal($"{++index}", pattern.ToString());
            }
            Assert.Equal(2, index);
        }
    }

    // Dummy PatternList for testing; replace with full logic in integration.
    public class PatternList : IEnumerable<Regex>
    {
        private readonly List<Regex> _patterns;

        public PatternList(params string[] patterns)
        {
            if (patterns == null)
                throw new ArgumentNullException();
            _patterns = new List<Regex>();
            foreach (var p in patterns)
            {
                try
                {
                    _patterns.Add(new Regex(p));
                }
                catch (Exception)
                {
                    throw new ArgumentException();
                }
            }
        }

        public IEnumerator<Regex> GetEnumerator() => _patterns.GetEnumerator();

        System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() => GetEnumerator();
    }
}