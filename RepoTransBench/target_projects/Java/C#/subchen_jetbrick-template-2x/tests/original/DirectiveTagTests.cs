using System;
using System.IO;
using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class DirectiveTagTests : AbstractJetxTest
    {
        public override void InitializeEngine()
        {
            engine.GlobalResolver.RegisterTags(typeof(Tags));
        }

        [Fact]
        public void Test()
        {
            Assert.Equal("hello", Eval("#tag hello()#end"));
            Assert.Equal("hello", Eval("#tag hello()XXX#end"));
            Assert.Equal("hello:XXX", Eval("#tag helloWithBody()XXX#end"));
            Assert.Equal("hello:jetbrick:XXX", Eval("#tag helloWithParam('jetbrick')XXX#end"));
        }

        [Fact]
        public void TestClosure()
        {
            Assert.Equal("hello:1", Eval("#set(i=1)#tag helloWithBody()${i}#end"));
            Assert.Equal("hello:19", Eval("#set(i=1)#tag helloWithBody()${i}#set(x=9)#end${x}"));
        }

        [Fact]
        public void TestNotFound()
        {
            var ex = Assert.Throws<InterpretException>(() => Eval("#tag hello(1)#end"));
            Assert.Contains(Err(Errors.TAG_NOT_FOUND), ex.Message);
        }

        public static class Tags
        {
            public static void Hello(JetTagContext ctx)
            {
                ctx.Writer.Write("hello");
            }

            public static void HelloWithBody(JetTagContext ctx)
            {
                ctx.Writer.Write("hello:" + ctx.BodyContent);
            }

            public static void HelloWithParam(JetTagContext ctx, string name)
            {
                ctx.Writer.Write($"hello:{name}:");
                ctx.Invoke();
            }
        }
    }
}