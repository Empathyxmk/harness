using System;
using System.Collections.Generic;
using System.Data;
using Moq;
using Xunit;
using Jkrasnay.SqlBuilder.Orm;

namespace Jkrasnay.SqlBuilder.Tests.Original.Orm
{
    public class StringListConverterTests
    {
        private void AssertConvert(StringListConverter converter, string s, List<string> list)
        {
            var rsMock = new Mock<IDataReader>();
            rsMock.Setup(r => r[s != null ? It.IsAny<string>() : "columnName"]).Returns(s);
            var rs = rsMock.Object;
            Assert.Equal(list, converter.GetFieldValueFromResultSet(rs, "columnName"));
            Assert.Equal(s, converter.ConvertFieldValueToColumn(list));
        }

        [Fact]
        public void TestAll()
        {
            var list = new List<string>();
            var converter = new StringListConverter();

            AssertConvert(converter, "", list);

            list.Add("foo");
            AssertConvert(converter, "foo", list);

            list.Add("bar");
            AssertConvert(converter, "foo,bar", list);

            list.Add("b\\a,z");
            AssertConvert(converter, "foo,bar,b\\\\a\\,z", list);
        }

        [Fact]
        public void TestNullResultsInEmptyList()
        {
            var rsMock = new Mock<IDataReader>();
            rsMock.Setup(r => r["columnName"]).Returns((string)null);
            var rs = rsMock.Object;

            var converter = new StringListConverter();
            var value = converter.GetFieldValueFromResultSet(rs, "columnName");

            Assert.NotNull(value);
            Assert.Equal(0, value.Count);
        }
    }
}