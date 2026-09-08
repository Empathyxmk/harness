using System;
using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.PublicTests
{
    public class AbstractSqlCreatorPublicTests
    {
        [Fact]
        public void AllocatesParametersSequentially()
        {
            var sc = new SelectCreator();
            Assert.Equal("param0", sc.AllocateParameter());
            Assert.Equal("param1", sc.AllocateParameter());
            Assert.Equal("param2", sc.AllocateParameter());
        }
    }
}