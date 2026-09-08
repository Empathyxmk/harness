using System;
using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.PublicTests
{
    public class SelectBuilderPublicTests
    {
        [Fact]
        public void SelectBuilderCreatesProperSql()
        {
            var builder = new SelectBuilder("tbl").Column("col1").Where("id = 1").OrderBy("col1");
            Assert.Equal("select col1 from tbl where id = 1 order by col1", builder.ToString());
        }

        [Fact]
        public void UnionSelectsAreSupported()
        {
            var sb1 = new SelectBuilder().Column("a").From("TA").Where("a > 1");
            var sb2 = new SelectBuilder().Column("a").From("TB");
            sb1.Union(sb2);

            Assert.Equal("select a from TA where a > 1 union select a from TB", sb1.ToString());
        }
    }
}