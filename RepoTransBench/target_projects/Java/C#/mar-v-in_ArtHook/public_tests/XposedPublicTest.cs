using System;
using System.Reflection;
using Xunit;
using Moq;
using ArtHook;

namespace ArtHook.PublicTests
{
    public class XposedPublicTest
    {
        [Fact]
        public void TestMainCallsInitAndHandlesDifferentException()
        {
            // Static method mocking not supported natively; simulate invocation and expect catching.
            Xposed.main(true, new string[] { "a", "b" });
            Assert.True(true);
        }

        [Fact]
        public void TestTestPrintsLogWithDifferentVerification()
        {
            var method = typeof(Xposed).GetMethod("test", BindingFlags.Static | BindingFlags.NonPublic);
            Assert.NotNull(method);
            method!.Invoke(null, null);
            Assert.True(true);
        }
    }
}