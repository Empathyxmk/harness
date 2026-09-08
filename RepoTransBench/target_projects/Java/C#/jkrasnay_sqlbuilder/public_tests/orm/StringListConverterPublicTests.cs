using System.Collections.Generic;
using Xunit;
using Jkrasnay.SqlBuilder.Orm;

namespace Jkrasnay.SqlBuilder.PublicTests.Orm
{
    public class StringListConverterPublicTests
    {
        [Fact]
        public void CanConvertEmptyStringToEmptyList()
        {
            var converter = new StringListConverter();
            var result = converter.Split("");
            Assert.Empty(result);
        }
    }
}