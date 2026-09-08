using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.PublicTests
{
    public class DeleteBuilderPublicTests
    {
        [Fact]
        public void GeneratesCorrectDeleteSql()
        {
            var builder = new DeleteBuilder("Foo");
            Assert.Equal("delete from Foo", builder.ToString());

            builder = new DeleteBuilder("Foo").Where("id = 1");
            Assert.Equal("delete from Foo where id = 1", builder.ToString());

            builder = new DeleteBuilder("Foo").Where("id = 1").Where("colour = 'red'");
            Assert.Equal("delete from Foo where id = 1 and colour = 'red'", builder.ToString());
        }
    }
}