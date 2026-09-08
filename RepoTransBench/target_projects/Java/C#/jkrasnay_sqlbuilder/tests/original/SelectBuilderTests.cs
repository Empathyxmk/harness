using System;
using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.Tests.Original
{
    public class SelectBuilderTests
    {
        [Fact]
        public void TestBasics()
        {
            SelectBuilder sb;

            // Simple tables
            sb = new SelectBuilder("Employee");
            Assert.Equal("select * from Employee", sb.ToString());

            sb = new SelectBuilder("Employee e");
            Assert.Equal("select * from Employee e", sb.ToString());

            sb = new SelectBuilder("Employee e").Column("name");
            Assert.Equal("select name from Employee e", sb.ToString());

            sb = new SelectBuilder("Employee e").Column("name").Column("age");
            Assert.Equal("select name, age from Employee e", sb.ToString());

            sb = new SelectBuilder("Employee e").Column("name as n").Column("age");
            Assert.Equal("select name as n, age from Employee e", sb.ToString());

            // Where clauses
            sb = new SelectBuilder("Employee e").Where("name like 'Bob%'");
            Assert.Equal("select * from Employee e where name like 'Bob%'", sb.ToString());

            sb = new SelectBuilder("Employee e").Where("name like 'Bob%'").Where("age > 37");
            Assert.Equal("select * from Employee e where name like 'Bob%' and age > 37", sb.ToString());

            // Join clauses
            sb = new SelectBuilder("Employee e").Join("Department d on e.dept_id = d.id");
            Assert.Equal("select * from Employee e join Department d on e.dept_id = d.id", sb.ToString());

            sb = new SelectBuilder("Employee e")
                .Join("Department d on e.dept_id = d.id")
                .Where("name like 'Bob%'");
            Assert.Equal("select * from Employee e join Department d on e.dept_id = d.id where name like 'Bob%'", sb.ToString());

            // Order by clauses
            sb = new SelectBuilder("Employee e").OrderBy("name");
            Assert.Equal("select * from Employee e order by name", sb.ToString());

            sb = new SelectBuilder("Employee e").OrderBy("name desc").OrderBy("age");
            Assert.Equal("select * from Employee e order by name desc, age", sb.ToString());

            sb = new SelectBuilder("Employee").Where("name like 'Bob%'").OrderBy("age");
            Assert.Equal("select * from Employee where name like 'Bob%' order by age", sb.ToString());

            // For Update
            sb = new SelectBuilder("Employee").Where("id = 42").ForUpdate();
            Assert.Equal("select * from Employee where id = 42 for update", sb.ToString());
        }

        [Fact]
        public void TestLimits()
        {
            var sb = new SelectBuilder()
                .From("test_table")
                .Column("a")
                .Column("b")
                .Limit(10);

            Assert.Equal("select a, b from test_table limit 10", sb.ToString());

            sb = sb.Limit(10, 4);

            Assert.Equal("select a, b from test_table limit 10, 4", sb.ToString());
        }

        [Fact]
        public void TestUnions()
        {
            SelectBuilder sb = new SelectBuilder()
                .Column("a")
                .Column("b")
                .From("Foo")
                .Where("a > 10")
                .OrderBy("1");

            sb.Union(new SelectBuilder()
                .Column("c")
                .Column("d")
                .From("Bar"));

            Assert.Equal("select a, b from Foo where a > 10 union select c, d from Bar order by 1", sb.ToString());
        }
    }
}