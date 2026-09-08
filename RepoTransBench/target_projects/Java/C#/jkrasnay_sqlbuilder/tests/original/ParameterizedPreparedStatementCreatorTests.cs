using System;
using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.Tests.Original
{
    public class ParameterizedPreparedStatementCreatorTests
    {
        private void AssertResult(ParameterizedPreparedStatementCreator ppsc, string psSql, params object[] expectedParams)
        {
            var sap = ppsc.CreateSqlAndParams();
            Assert.Equal(psSql, sap.Sql);
            Assert.Equal(expectedParams.Length, sap.Params.Count);
            for (int i = 0; i < expectedParams.Length; i++)
                Assert.Equal(expectedParams[i], sap.Params[i]);
        }

        [Fact]
        public void TestAll()
        {
            ParameterizedPreparedStatementCreator ppsc;

            ppsc = new ParameterizedPreparedStatementCreator().SetSql("");
            AssertResult(ppsc, "");

            ppsc = new ParameterizedPreparedStatementCreator().SetSql("select * from Employee");
            AssertResult(ppsc, "select * from Employee");

            ppsc = new ParameterizedPreparedStatementCreator().SetSql("select * from Employee where name = :name");
            Assert.Throws<ArgumentException>(() =>
            {
                ppsc.CreateSqlAndParams();
            });

            ppsc = new ParameterizedPreparedStatementCreator()
                .SetSql("select * from Employee where name = :name")
                .SetParameter("name", "Joe");
            AssertResult(ppsc, "select * from Employee where name = ?", "Joe");

            ppsc = new ParameterizedPreparedStatementCreator()
                .SetSql("select * from Employee where name = :name and age > 37")
                .SetParameter("name", "Joe");
            AssertResult(ppsc, "select * from Employee where name = ? and age > 37", "Joe");

            ppsc = new ParameterizedPreparedStatementCreator()
                .SetSql("select * from Employee where name = :name and age > :age")
                .SetParameter("name", "Joe")
                .SetParameter("age", 37);
            AssertResult(ppsc, "select * from Employee where name = ? and age > ?", "Joe", 37);
        }
    }
}