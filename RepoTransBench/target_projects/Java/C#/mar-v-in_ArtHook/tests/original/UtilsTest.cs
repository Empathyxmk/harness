using System;
using Xunit;
using ArtHook;

namespace ArtHook
{
    public static class DummyMain
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

namespace ArtHook.Tests.Original
{
    public class UtilsTest
    {
        [Fact]
        public void TestCallMainSuccessful()
        {
            ArtHook.DummyMain.Called = false;
            ArtHook.DummyMain.Throwable = null;
            Utils.callMain(typeof(ArtHook.DummyMain).FullName!);
            Assert.True(ArtHook.DummyMain.Called);
        }

        [Fact]
        public void TestCallMainThrowsTargetException()
        {
            ArtHook.DummyMain.Called = false;
            ArtHook.DummyMain.Throwable = new Exception("test");
            Assert.Throws<Exception>(() => Utils.callMain(typeof(ArtHook.DummyMain).FullName!));
        }
    }
}