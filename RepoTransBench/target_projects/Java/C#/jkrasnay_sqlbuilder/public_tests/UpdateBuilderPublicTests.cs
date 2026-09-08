using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.PublicTests
{
    public class UpdateBuilderPublicTests
    {
        [Fact]
        public void UpdateBuilderProducesValidSql()
        {
            var builder = new UpdateBuilder("T");
            builder.Set("col1 = 1");
            Assert.Equal("update T set col1 = 1", builder.ToString());
        }
    }
}