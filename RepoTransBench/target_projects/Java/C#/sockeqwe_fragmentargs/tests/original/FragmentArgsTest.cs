using System;
using System.Reflection;
using Xunit;

namespace ProjectName.Tests.Original
{
    public class FragmentArgsTest
    {
        // Dummy interface from the library under test
        public interface IFragmentArgsInjector
        {
            void Inject(object target);
        }

        public class DummyInjector : IFragmentArgsInjector
        {
            public bool Injected = false;
            public void Inject(object target)
            {
                Injected = true;
            }
        }

        // Simulate static field in FragmentArgs class
        public static class FragmentArgs
        {
            public static IFragmentArgsInjector? autoMappingInjector { get; set; }
            public static void Inject(object target)
            {
                autoMappingInjector?.Inject(target);
            }
        }

        [Fact]
        public void TestInjectWithNoAutoMappingClass()
        {
            // Should not throw even if injector cannot be found.
            FragmentArgs.autoMappingInjector = null;
            FragmentArgs.Inject(new object());
        }

        [Fact]
        public void TestInjectWithAutoMappingInjectorPresent()
        {
            // Reflection hack to inject DummyInjector (simulate static field).
            var dummy = new DummyInjector();
            FragmentArgs.autoMappingInjector = dummy;

            object fragment = new object();
            FragmentArgs.Inject(fragment);
            Assert.True(dummy.Injected);

            // Clean up for other tests.
            FragmentArgs.autoMappingInjector = null;
        }
    }
}