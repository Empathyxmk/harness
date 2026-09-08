using System;
using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.Tests.Original
{
    public class InsertBuilderTests
    {
        [Fact]
        public void TestAll()
        {
            InsertBuilder builder;

            builder = new InsertBuilder("Employee");
            Assert.Equal("insert into Employee () values ()", builder.ToString());

            builder.Set("id", "1");
            Assert.Equal("insert into Employee (id) values (1)", builder.ToString());

            builder.Set("name", "'Bobo'");
            Assert.Equal("insert into Employee (id, name) values (1, 'Bobo')", builder.ToString());
        }
    }
}