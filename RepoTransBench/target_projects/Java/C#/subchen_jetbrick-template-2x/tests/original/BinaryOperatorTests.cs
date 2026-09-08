using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class BinaryOperatorTests : AbstractJetxTest
    {
        [Fact]
        public void TestPlus()
        {
            Assert.Equal("3", Eval("${1+2}"));
            Assert.Equal("3", Eval("${1+2L}"));
            Assert.Equal("3.1", Eval("${1+2.1f}"));
            Assert.Equal("3.1", Eval("${1+2.1d}"));
        }

        [Fact]
        public void TestMinus()
        {
            Assert.Equal("1", Eval("${2-1}"));
            Assert.Equal("1", Eval("${2L-1}"));
            Assert.Equal("0.9", Eval("${2-1.1f}"));
            Assert.Equal("0.9", Eval("${2-1.1f}"));
        }

        [Fact]
        public void TestMul()
        {
            Assert.Equal("6", Eval("${2*3}"));
            Assert.Equal("6", Eval("${2*3L}"));
            Assert.Equal("6.2", Eval("${2*3.1f}"));
            Assert.Equal("6.2", Eval("${2*3.1d}"));
        }

        [Fact]
        public void TestDiv()
        {
            Assert.Equal("1", Eval("${6/4}"));
            Assert.Equal("1", Eval("${6/4L}"));
            Assert.Equal("1.5", Eval("${6/4f}"));
            Assert.Equal("1.5", Eval("${6/4d}"));
        }

        [Fact]
        public void TestMod()
        {
            Assert.Equal("1", Eval("${3%2}"));
            Assert.Equal("1", Eval("${3%2L}"));
            Assert.Equal("1.0", Eval("${3%2f}"));
            Assert.Equal("1.0", Eval("${3%2d}"));
        }

        [Fact]
        public void TestArithmetic()
        {
            Assert.Equal("7.2", Eval("${1+2*3.1}"));
            Assert.Equal("2.2", Eval("${1.1+1.1}"));
            Assert.Equal("-10.2", Eval("${1+2*(3-4)*5.6}"));
        }

        [Fact]
        public void TestStringAdd()
        {
            Assert.Equal("a1", Eval("${'a'+1}"));
            Assert.Equal("1a", Eval("${1+'a'}"));
            Assert.Equal("12", Eval("${'1'+'2'}"));
            Assert.Equal("a", Eval("${'a'+null}"));
            Assert.Equal("a", Eval("${null+'a'}"));
        }

        [Fact]
        public void TestInstanceOf()
        {
            Assert.Equal("true", Eval("${'a' instanceof String}"));
            Assert.Equal("true", Eval("${1 instanceof Number}"));
            Assert.Equal("false", Eval("${'a' instanceof Number}"));
        }

        [Fact]
        public void TestNullAsDefault()
        {
            Assert.Equal("0", Eval("${a ?! 0}"));
            Assert.Equal("0", Eval("${a.b.c ?! 0}"));
            Assert.Equal("0", Eval("${a.b() ?! 0}"));
            Assert.Equal("0", Eval("${a[0] ?! 0}"));
        }
    }
}