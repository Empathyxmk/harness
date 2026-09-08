using System;
using System.IO;
using System.Reflection;
using Xunit;
using CaoymJjvm;
using CaoymJjvm.Lang;
using CaoymJjvm.Natives;

namespace CaoymJjvm.Tests.Original
{
    public class JvmDefaultClassLoaderTest
    {
        public class DummyNativeClass : JvmNativeClass
        {
            public DummyNativeClass(IJvmClassLoader loader, Type hostClass)
                : base(loader, hostClass)
            { }
        }

        [Fact]
        public void TestNonExistingClassLoadsAsNative()
        {
            // should never find a .class file with this name, so will hit native branch
            // fallback to load a .NET type as a native class
            var loader = new JvmDefaultClassLoader(System.IO.Path.GetFullPath("."));
            // Use a well-known .NET type (string) as the native class
            var c = loader.LoadClass("System.String");
            Assert.NotNull(c);
            Assert.IsType<JvmNativeClass>(c);
        }

        [Fact]
        public void TestConstructorAndClassPath()
        {
            var fakePath = "/tmp";
            var loader = new JvmDefaultClassLoader(fakePath);
            Assert.NotNull(loader);
        }
    }
}