using System;
using Xunit;
using ArtHook;

namespace ArtHook
{
    public static class DummyPublicMain
    {
        public static bool Called = false;
        public static Exception? Throwable = null;

        public static void main(string[] args)
        {
            Called = true;
            if (Throwable != null)
                throw Throwable;
        }
    }
}

namespace ArtHook.PublicTests
{
    public class UtilsPublicTest
    {
        [Fact]
        public void TestCallMainSuccessfulWithDifferentClass()
        {
            ArtHook.DummyPublicMain.Called = false;
            ArtHook.DummyPublicMain.Throwable = null;
            Utils.callMain(typeof(ArtHook.DummyPublicMain).FullName!);
            Assert.True(ArtHook.DummyPublicMain.Called);
        }

        [Fact]
        public void TestCallMainThrowsTargetRuntimeException()
        {
            ArtHook.DummyPublicMain.Called = false;
            ArtHook.DummyPublicMain.Throwable = new InvalidOperationException("public test");
            Assert.Throws<InvalidOperationException>(() => Utils.callMain(typeof(ArtHook.DummyPublicMain).FullName!));
        }
    }
}