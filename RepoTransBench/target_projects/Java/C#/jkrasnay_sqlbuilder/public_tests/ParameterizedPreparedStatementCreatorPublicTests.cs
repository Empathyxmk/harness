using System;
using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.PublicTests
{
    public class ParameterizedPreparedStatementCreatorPublicTests
    {
        private void AssertResult(ParameterizedPreparedStatementCreator ppsc, string expectedSql, params object[] expectedParams)
        {
            var sap = ppsc.CreateSqlAndParams();
            Assert.Equal(expectedSql, sap.Sql);
            Assert.Equal(expectedParams.Length, sap.Params.Count);
            for (int i = 0; i < expectedParams.Length; i++)
                Assert.Equal(expectedParams[i], sap.Params[i]);
        }

        [Fact]
        public void ParameterizedStatementsWork()
        {
            var ppsc = new ParameterizedPreparedStatementCreator()
                .SetSql("select * from table where foo = :bar")
                .SetParameter("bar", 42);
            AssertResult(ppsc, "select * from table where foo = ?", 42);

            ppsc = new ParameterizedPreparedStatementCreator().SetSql("foo :one and :two").SetParameter("one", 1).SetParameter("two", 2);
            AssertResult(ppsc, "foo ? and ?", 1, 2);
        }
    }
}