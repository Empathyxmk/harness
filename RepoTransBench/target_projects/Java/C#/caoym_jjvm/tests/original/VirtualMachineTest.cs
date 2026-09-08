using System;
using System.IO;
using System.Reflection;
using System.Collections.Generic;
using Xunit;
using CaoymJjvm;
using CaoymJjvm.Lang;

namespace CaoymJjvm.Tests.Original
{
    public class VirtualMachineTest
    {
        class DummyMethod : IJvmMethod
        {
            public bool Called = false;
            public void Call(object env, object thiz, params object[] args) { Called = true; }
            public int GetParameterCount() => 1;
            public string GetName() => "main";
        }

        class DummyClass : JvmClass
        {
            public DummyMethod Method = new DummyMethod();

            public DummyClass()
                : base(
                    null, null, null, null,
                    null, null, null, null, false)
            { }

            public override IJvmMethod? GetMethod(string name, string descriptor)
            {
                if (name == "main" && descriptor == "([Ljava/lang/String;)V")
                    return Method;
                return null;
            }
        }

        class DummyClassLoader : IJvmClassLoader
        {
            public bool Loaded = false;
            public JvmClass LoadClass(string className)
            {
                Loaded = true;
                return new DummyClass();
            }
        }

        [Fact]
        public void TestGetClass_CachesAndReturns()
        {
            var vm = new VirtualMachine(System.IO.Path.GetFullPath("."), "FakeClass");

            // Use reflection to set private classLoader field to dummy loader
            var type = typeof(VirtualMachine);
            var f = type.GetField("classLoader", BindingFlags.Instance | BindingFlags.NonPublic);
            var loader = new DummyClassLoader();
            f.SetValue(vm, loader);

            var cls1 = vm.GetClass("hello.FakeClass");
            Assert.True(loader.Loaded);
            loader.Loaded = false;

            var cls2 = vm.GetClass("hello.FakeClass");
            Assert.False(loader.Loaded);
            Assert.Same(cls1, cls2);
        }
    }
}