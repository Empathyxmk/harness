using System;
using System.Collections.Generic;
using System.Data;
using Moq;
using Xunit;
using Jkrasnay.SqlBuilder.Orm;

namespace Jkrasnay.SqlBuilder.Tests.Original.Orm
{
    public class StringMapConverterTests
    {
        private void AssertConvert(StringMapConverter converter, string s, Dictionary<string, string> map)
        {
            var rsMock = new Mock<IDataReader>();
            rsMock.Setup(r => r[s != null ? It.IsAny<string>() : "columnName"]).Returns(s);
            var rs = rsMock.Object;
            AssertMapEquals(map, converter.GetFieldValueFromResultSet(rs, "columnName"));
            Assert.Equal(s, converter.ConvertFieldValueToColumn(map));
        }

        private void AssertMapEquals(Dictionary<string, string> expected, Dictionary<string, string> actual)
        {
            Assert.Equal(expected.Count, actual.Count);
            foreach (var kv in expected)
            {
                Assert.True(actual.ContainsKey(kv.Key), $"Expected key {kv.Key}");
                Assert.Equal(kv.Value, actual[kv.Key]);
            }
        }

        [Fact]
        public void TestAll()
        {
            var map = new Dictionary<string, string>();
            var converter = new StringMapConverter();

            AssertConvert(converter, "", map);

            map["foo"] = "bar";
            AssertConvert(converter, "foo=bar", map);

            map["b\\a,z"] = "q\\uu,x";
            AssertConvert(converter, "foo=bar,b\\\\a\\,z=q\\\\uu\\,x", map);
        }

        [Fact]
        public void TestNullResultsInEmptyMap()
        {
            var rsMock = new Mock<IDataReader>();
            rsMock.Setup(r => r["columnName"]).Returns((string)null);
            var rs = rsMock.Object;

            var converter = new StringMapConverter();
            var value = converter.GetFieldValueFromResultSet(rs, "columnName");

            Assert.NotNull(value);
            Assert.Equal(0, value.Count);
        }
    }
}