using System;
using Xunit;
using CaoymJjvm;

namespace CaoymJjvm.PublicTests
{
    public class JJvmPublicTest
    {
        [Fact]
        public void TestMainMethodInvocationWithDifferentArgs()
        {
            string[] args = new[] { "foo", "bar", "baz" };
            var jvm = new JJvm();
            Exception? ex = Record.Exception(() => jvm.Main(new[] { "-version" }));
            Assert.Null(ex);
        }

        [Fact]
        public void TestCustomArgsToMain()
        {
            string[] inputArgs = new[] { "-help" };
            var jvm = new JJvm();
            Exception? ex = Record.Exception(() => jvm.Main(inputArgs));
            Assert.Null(ex);
        }
    }
}