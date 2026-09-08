using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.PublicTests
{
    public class SelectCreatorPublicTests
    {
        [Fact]
        public void WhereInBindsParameters()
        {
            var sc = new SelectCreator()
                .Column("id")
                .From("users")
                .WhereIn("name", new[] { "a", "b" });
            Assert.Equal("select id from users where name in (:param0, :param1)", sc.Builder.ToString());

            var ppsc = sc.PreparedStatementCreator;
            var map = ppsc.ParameterMap;

            Assert.Equal("a", map["param0"]);
            Assert.Equal("b", map["param1"]);
        }
    }
}