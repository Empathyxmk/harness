using System;
using System.Collections.Generic;
using Xunit;
using Jkrasnay.SqlBuilder;
using static Jkrasnay.SqlBuilder.Predicates;

namespace Jkrasnay.SqlBuilder.Tests.Original
{
    public class PredicateTests
    {
        [Fact]
        public void TestEq()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp")
                .Where(Eq("name", "Bob"));

            Assert.Equal("select * from Emp where name = :param0", sc.Builder.ToString());
            Assert.Equal("Bob", sc.PreparedStatementCreator.ParameterMap["param0"]);
        }

        [Fact]
        public void TestExists()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp e")
                .Where(Exists("SickDay sd").Where("sd.emp_id = e.id").And(Eq("sd.dow", "Monday")));

            Assert.Equal("select * from Emp e where exists (select 1 from SickDay sd where sd.emp_id = e.id and sd.dow = :param0)", sc.Builder.ToString());
            Assert.Equal("Monday", sc.PreparedStatementCreator.ParameterMap["param0"]);
        }

        [Fact]
        public void TestInArray()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp")
                .Where(In("name", "Larry", "Curly", "Moe"));

            Assert.Equal("select * from Emp where name in (:param0, :param1, :param2)", sc.Builder.ToString());

            var map = sc.PreparedStatementCreator.ParameterMap;
            Assert.Equal("Larry", map["param0"]);
            Assert.Equal("Curly", map["param1"]);
            Assert.Equal("Moe", map["param2"]);
        }

        [Fact]
        public void TestInList()
        {
            var names = new List<string> { "Larry", "Curly", "Moe" };
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp")
                .Where(In("name", names));

            Assert.Equal("select * from Emp where name in (:param0, :param1, :param2)", sc.Builder.ToString());

            var map = sc.PreparedStatementCreator.ParameterMap;
            Assert.Equal("Larry", map["param0"]);
            Assert.Equal("Curly", map["param1"]);
            Assert.Equal("Moe", map["param2"]);
        }

        [Fact]
        public void TestNot()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp")
                .Where(Not(Eq("name", "Bob")));

            Assert.Equal("select * from Emp where not (name = :param0)", sc.Builder.ToString());
            Assert.Equal("Bob", sc.PreparedStatementCreator.ParameterMap["param0"]);
        }

        [Fact]
        public void TestIsNull()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp")
                .Where(IsNull("name"));
            Assert.Equal("select * from Emp where name is null", sc.Builder.ToString());
        }

        [Fact]
        public void TestIsNotNull()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp")
                .Where(IsNotNull("name"));
            Assert.Equal("select * from Emp where name is not null", sc.Builder.ToString());
        }

        [Fact]
        public void TestGt()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp")
                .Where(Gt("rank", "1"));

            Assert.Equal("select * from Emp where rank > :param0", sc.Builder.ToString());
            Assert.Equal("1", sc.PreparedStatementCreator.ParameterMap["param0"]);
        }

        [Fact]
        public void TestGte()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp")
                .Where(Gte("rank", "1"));

            Assert.Equal("select * from Emp where rank >= :param0", sc.Builder.ToString());
            Assert.Equal("1", sc.PreparedStatementCreator.ParameterMap["param0"]);
        }

        [Fact]
        public void TestLt()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp")
                .Where(Lt("rank", "1"));

            Assert.Equal("select * from Emp where rank < :param0", sc.Builder.ToString());
            Assert.Equal("1", sc.PreparedStatementCreator.ParameterMap["param0"]);
        }

        [Fact]
        public void TestLte()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp")
                .Where(Lte("rank", "1"));

            Assert.Equal("select * from Emp where rank <= :param0", sc.Builder.ToString());
            Assert.Equal("1", sc.PreparedStatementCreator.ParameterMap["param0"]);
        }

        [Fact]
        public void TestLike()
        {
            var sc = new SelectCreator()
                .Column("*")
                .From("Emp")
                .Where(Like("name", "Bob"));

            Assert.Equal("select * from Emp where name like ':param0'", sc.Builder.ToString());
            Assert.Equal("Bob", sc.PreparedStatementCreator.ParameterMap["param0"]);
        }
    }
}