using System;
using Xunit;
using Jkrasnay.SqlBuilder.Orm;

namespace Jkrasnay.SqlBuilder.PublicTests.Orm
{
    public class MappingPublicTests
    {
        public class X
        {
            public int id;
            public string name;
        }

        [Fact]
        public void MappingFindByIdThrowsOnMissing()
        {
            Assert.Throws<RowNotFoundException>(() =>
            {
                var ormConfig = new OrmConfig("Fake", new PostgresqlDialect());
                var mapping = new Mapping<X>(ormConfig, typeof(X), "X")
                    .SetIdColumn(new Column("id"))
                    .AddColumn("name");
                mapping.FindById(1000);
            });
        }
    }
}