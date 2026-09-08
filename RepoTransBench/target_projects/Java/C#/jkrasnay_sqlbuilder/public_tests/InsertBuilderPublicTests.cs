using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.PublicTests
{
    public class InsertBuilderPublicTests
    {
        [Fact]
        public void InsertSqlIsCorrect()
        {
            var builder = new InsertBuilder("TestTable");
            Assert.Equal("insert into TestTable () values ()", builder.ToString());

            builder.Set("id", "1");
            Assert.Equal("insert into TestTable (id) values (1)", builder.ToString());

            builder.Set("col", "'val'");
            Assert.Equal("insert into TestTable (id, col) values (1, 'val')", builder.ToString());
        }
    }
}