using Xunit;
using Jkrasnay.SqlBuilder;
using static Jkrasnay.SqlBuilder.Predicates;

namespace Jkrasnay.SqlBuilder.PublicTests
{
    public class PredicatePublicTests
    {
        [Fact]
        public void EqCreatesSqlAndParameters()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("T")
                .Where(Eq("a", 7));
            Assert.Equal("select * from T where a = :param0", sc.Builder.ToString());
            Assert.Equal(7, sc.PreparedStatementCreator.ParameterMap["param0"]);
        }

        [Fact]
        public void InCreatesMultipleParameters()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("X")
                .Where(In("type", 1, 2, 3));
            Assert.Equal("select * from X where type in (:param0, :param1, :param2)", sc.Builder.ToString());

            var map = sc.PreparedStatementCreator.ParameterMap;
            Assert.Equal(1, map["param0"]);
            Assert.Equal(2, map["param1"]);
            Assert.Equal(3, map["param2"]);
        }
    }
}