using System;
using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.Tests.Original
{
    public class UpdateBuilderTests
    {
        [Fact]
        public void TestAll()
        {
            UpdateBuilder ub;

            ub = new UpdateBuilder("Employee");
            Assert.Equal("update Employee", ub.ToString());

            ub.Set("name = 'Bobo'");
            Assert.Equal("update Employee set name = 'Bobo'", ub.ToString());

            ub.Set("age = 37");
            Assert.Equal("update Employee set name = 'Bobo', age = 37", ub.ToString());

            ub.Where("name = 'Arnold'");
            Assert.Equal("update Employee set name = 'Bobo', age = 37 where name = 'Arnold'", ub.ToString());

            ub.Where("age = 17");
            Assert.Equal("update Employee set name = 'Bobo', age = 37 where name = 'Arnold' and age = 17", ub.ToString());
        }
    }
}