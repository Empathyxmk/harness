using System;
using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.Tests.Original
{
    public class AbstractSqlCreatorTests
    {
        [Fact]
        public void TestAllocateParameter()
        {
            var sc = new SelectCreator();
            Assert.Equal("param0", sc.AllocateParameter());
            Assert.Equal("param1", sc.AllocateParameter());
            Assert.Equal("param2", sc.AllocateParameter());
        }
    }
}