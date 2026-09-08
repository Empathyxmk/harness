using System.Collections.Generic;
using Xunit;
using Jkrasnay.SqlBuilder.Orm;

namespace Jkrasnay.SqlBuilder.PublicTests.Orm
{
    public class StringMapConverterPublicTests
    {
        [Fact]
        public void ConvertsEmptyStringToEmptyMap()
        {
            var converter = new StringMapConverter();
            var map = converter.Split("");
            Assert.NotNull(map);
            Assert.Empty(map);
        }
    }
}