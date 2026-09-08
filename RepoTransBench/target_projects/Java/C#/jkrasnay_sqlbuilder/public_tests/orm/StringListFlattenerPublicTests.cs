using System.Collections.Generic;
using Xunit;
using Jkrasnay.SqlBuilder.Orm;

namespace Jkrasnay.SqlBuilder.PublicTests.Orm
{
    public class StringListFlattenerPublicTests
    {
        [Fact]
        public void JoinAndSplitRoundTrip()
        {
            var flattener = new StringListFlattener();
            var list = new List<string> { "a", "b", "c" };
            var s = flattener.Join(list);
            var result = flattener.Split(s);
            Assert.Equal(list, result);
        }
    }
}