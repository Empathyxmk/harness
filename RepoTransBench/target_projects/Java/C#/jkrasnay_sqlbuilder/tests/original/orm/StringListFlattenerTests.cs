using System;
using System.Collections.Generic;
using Xunit;
using Jkrasnay.SqlBuilder.Orm;

namespace Jkrasnay.SqlBuilder.Tests.Original.Orm
{
    public class StringListFlattenerTests
    {
        [Fact]
        public void TestAll()
        {
            var slf = new StringListFlattener();

            var list = slf.Split(null);
            Assert.NotNull(list);
            Assert.Equal(0, list.Count);

            list = new List<string>();
            AssertEquivalent(list, "");

            list.Add(null);

            try
            {
                Assert.Equal("", new StringListFlattener().Join(list));
                Assert.True(false, "Expected exception for null entry in list");
            }
            catch (ArgumentException)
            {
            }

            list.Clear();
            list.Add("foo");
            AssertEquivalent(list, "foo");

            list.Add("bar");
            AssertEquivalent(list, "foo,bar");

            list.Add("b\\a,z");
            AssertEquivalent(list, "foo,bar,b\\\\a\\,z");

            list.Add("quux");
            AssertEquivalent(list, "foo,bar,b\\\\a\\,z,quux");

            list.Clear();
            list.Add("");
            list.Add("");
            list.Add("");

            AssertEquivalent(list, ",,");
        }

        [Fact]
        public void TestConvertEmptyToNull()
        {
            var slf = new StringListFlattener().SetConvertEmptyToNull(true);

            var list = slf.Split(null);
            Assert.NotNull(list);
            Assert.Equal(0, list.Count);

            list = new List<string>();
            AssertEquivalent(list, "");

            // Single null in list
            list.Add(null);
            Assert.Equal("", slf.Join(list));

            list.Add(null);
            Assert.Equal(",", slf.Join(list));

            var list2 = slf.Split(",");
            Assert.Equal(2, list2.Count);
            Assert.Null(list2[0]);
            Assert.Null(list2[1]);
        }

        private void AssertEquivalent(List<string> list, string flattened)
        {
            var slf = new StringListFlattener();
            Assert.Equal(flattened, slf.Join(list));
            Assert.Equal(list, slf.Split(flattened));
        }
    }
}