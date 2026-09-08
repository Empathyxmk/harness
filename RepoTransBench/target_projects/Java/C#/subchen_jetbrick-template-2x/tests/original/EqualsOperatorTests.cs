using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class EqualsOperatorTests : AbstractJetxTest
    {
        [Fact]
        public void TestTrue()
        {
            Assert.Equal("1", Eval("${(true)?1:0}"));
            Assert.Equal("0", Eval("${(false)?1:0}"));
            Assert.Equal("0", Eval("${(null)?1:0}"));
            Assert.Equal("1", Eval("${(1)?1:0}"));
            Assert.Equal("0", Eval("${(0)?1:0}"));
            Assert.Equal("1", Eval("${(1.0D)?1:0}"));
            Assert.Equal("0", Eval("${(0.0F)?1:0}"));
            Assert.Equal("1", Eval("${('a')?1:0}"));
            Assert.Equal("0", Eval("${([])?1:0}"));
            Assert.Equal("0", Eval("${({})?1:0}"));
            Assert.Equal("0", Eval("${(a)?1:0}"));
        }

        [Fact]
        public void TestCompare()
        {
            Assert.Equal("1", Eval("${(0==0)?1:0}"));
            Assert.Equal("1", Eval("${(0D==0.0F)?1:0}"));
            Assert.Equal("1", Eval("${(0D==0L)?1:0}"));
            Assert.Equal("1", Eval("${(1!=0)?1:0}"));
            Assert.Equal("1", Eval("${(1>0d)?1:0}"));
            Assert.Equal("1", Eval("${(1>=1)?1:0}"));
            Assert.Equal("1", Eval("${(1f>=0)?1:0}"));
            Assert.Equal("1", Eval("${(0<1)?1:0}"));
            Assert.Equal("1", Eval("${(0<=1)?1:0}"));
            Assert.Equal("1", Eval("${(0<=0)?1:0}"));
        }

        [Fact]
        public void TestComparable()
        {
            Assert.Equal("true", Eval("${'b' > 'a'}"));
            Assert.Equal("true", Eval("${'a' < 'b'}"));
            Assert.Equal("true", Eval("${'b' >= 'a'}"));
            Assert.Equal("true", Eval("${'a' >= 'a'}"));
            Assert.Equal("true", Eval("${'a' <= 'b'}"));
            Assert.Equal("true", Eval("${'a' <= 'a'}"));
        }

        [Fact]
        public void TestEquals()
        {
            Assert.Equal("true", Eval("${null==null}"));
            Assert.Equal("false", Eval("${1==null}"));
            Assert.Equal("false", Eval("${null==1}"));
        }

        [Fact]
        public void TestIdenticallyEquals()
        {
            Assert.Equal("true", Eval("${null===null}"));
            Assert.Equal("false", Eval("${'a'==='a'}"));
            Assert.Equal("false", Eval("${1===1L}"));
        }

        [Fact]
        public void TestAndOrNot()
        {
            Assert.Equal("false", Eval("${!true}"));
            Assert.Equal("true", Eval("${!false}"));
            Assert.Equal("true", Eval("${true && true}"));
            Assert.Equal("false", Eval("${true && false}"));
            Assert.Equal("false", Eval("${false && false}"));
            Assert.Equal("true", Eval("${true || true}"));
            Assert.Equal("true", Eval("${true || false}"));
            Assert.Equal("false", Eval("${false || false}"));
        }

        [Fact]
        public void TestAndOrQuickPath()
        {
            Assert.Equal("false", Eval("${false && [].get(0)}"));
            Assert.Equal("true", Eval("${true || [].get(0)}"));
        }
    }
}