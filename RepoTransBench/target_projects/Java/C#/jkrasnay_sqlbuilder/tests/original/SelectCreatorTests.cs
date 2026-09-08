using System;
using System.Collections.Generic;
using System.Reflection;
using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.Tests.Original
{
    public class SelectCreatorTests
    {
        private static object GetValue(object o, string field)
        {
            var f = o.GetType().GetField(field, BindingFlags.NonPublic | BindingFlags.Instance);
            if (f == null)
                throw new Exception($"Field '{field}' not found");
            return f.GetValue(o);
        }

        [Fact]
        public void TestWhereIn()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp")
                .WhereIn("name", new[] { "Larry", "Curly", "Moe" });

            var builder = (SelectBuilder)GetValue(sc, "builder");

            Assert.Equal("select * from Emp where name in (:param0, :param1, :param2)", builder.ToString());

            var ppsc = sc.PreparedStatementCreator;
            var map = ppsc.ParameterMap;

            Assert.Equal("Larry", map["param0"]);
            Assert.Equal("Curly", map["param1"]);
            Assert.Equal("Moe", map["param2"]);
        }
    }
}