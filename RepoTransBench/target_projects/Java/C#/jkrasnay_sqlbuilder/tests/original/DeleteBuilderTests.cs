using System;
using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.Tests.Original
{
    public class DeleteBuilderTests
    {
        [Fact]
        public void TestAll()
        {
            Assert.Equal("delete from Foo", new DeleteBuilder("Foo").ToString());
            Assert.Equal("delete from Foo where id = 1", new DeleteBuilder("Foo").Where("id = 1").ToString());
            Assert.Equal("delete from Foo where id = 1 and colour = 'red'",
                new DeleteBuilder("Foo").Where("id = 1").Where("colour = 'red'").ToString());
        }
    }
}