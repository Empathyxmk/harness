using Xunit;
using Jkrasnay.SqlBuilder.Orm;

namespace Jkrasnay.SqlBuilder.PublicTests.Orm
{
    public class ReflectionUtilsPublicTests
    {
        private class Foo
        {
            public string value;
        }

        [Fact]
        public void GetDeclaredFieldWithPathFindsDirect()
        {
            var field = ReflectionUtils.GetDeclaredFieldWithPath(typeof(Foo), "value");
            Assert.Equal("value", field.Name);
        }
    }
}