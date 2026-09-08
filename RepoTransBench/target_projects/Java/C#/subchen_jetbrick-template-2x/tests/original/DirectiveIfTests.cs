using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class DirectiveIfTests : AbstractJetxTest
    {
        [Fact]
        public void TestIf()
        {
            Assert.Equal("a", Eval("#if(true)a#end"));
            Assert.Equal("", Eval("#if(false)a#end"));
        }

        [Fact]
        public void TestElseIf()
        {
            Assert.Equal("1", Eval("#set(i=1)#if(i==0)0#elseif(i==1)1#elseif(i==2)2#end"));
            Assert.Equal("9", Eval("#set(i=3)#if(i==0)0#elseif(i==1)1#else()9#end"));
        }

        [Fact]
        public void TestElse()
        {
            Assert.Equal("a", Eval("#if(true)a#else()b#end"));
            Assert.Equal("b", Eval("#if(false)a#else()b#end"));
        }
    }
}