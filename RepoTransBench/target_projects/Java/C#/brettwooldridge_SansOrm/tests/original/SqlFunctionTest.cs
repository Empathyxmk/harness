using System;
using System.Data;
using System.Data.Common;
using Xunit;

namespace SansOrm.Tests.Original
{
    public class SqlFunctionTest
    {
        public delegate TResult SqlFunction<T, TResult>(T arg);

        [Fact]
        public void TestSqlFunctionExecute()
        {
            SqlFunction<IDbConnection, string> function = (connection) => "ok";
            Assert.Equal("ok", function(null));
        }

        [Fact]
        public void TestSqlFunctionExecuteThrows()
        {
            SqlFunction<IDbConnection, object> function = (connection) => throw new InvalidOperationException("fail");
            var ex = Assert.Throws<InvalidOperationException>(() => function(null));
            Assert.Equal("fail", ex.Message);
        }
    }
}