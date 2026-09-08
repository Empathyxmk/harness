using System;
using Xunit;
using CaoymJjvm;

namespace CaoymJjvm.PublicTests
{
    public class JvmDefaultClassLoaderPublicTest
    {
        [Fact]
        public void TestLoadResourceFileWithDifferentResource()
        {
            var loader = new JvmDefaultClassLoader();
            // Try some known resource name likely missed in private test
            Assert.Null(loader.GetResourceAsStream("META-INF/not-a-real-resource.txt"));
        }

        [Fact]
        public void TestNonExistingClassReturnsNull()
        {
            var loader = new JvmDefaultClassLoader();
            Assert.Null(loader.LoadClassBytes("com/example/NoSuchClass.class"));
        }
    }
}