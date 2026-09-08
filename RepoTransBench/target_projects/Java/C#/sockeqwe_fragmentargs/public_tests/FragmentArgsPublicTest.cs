using System;
using System.Reflection;
using Xunit;

namespace ProjectName.PublicTests
{
    public class FragmentArgsPublicTest
    {
        public interface IFragmentArgsInjector
        {
            void Inject(object target);
        }

        public class AlternateDummyInjector : IFragmentArgsInjector
        {
            public bool Invoked = false;
            public void Inject(object target)
            {
                if (target != null)
                    Invoked = true;
            }
        }

        public static class FragmentArgs
        {
            public static IFragmentArgsInjector? autoMappingInjector { get; set; }
            public static void Inject(object target)
            {
                autoMappingInjector?.Inject(target);
            }
        }

        [Fact]
        public void TestInjectWithNoAutoMappingClass_DifferentInput()
        {
            FragmentArgs.autoMappingInjector = null;
            FragmentArgs.Inject("publicDummyString");
        }

        [Fact]
        public void TestInjectWithAutoMappingInjectorPresent_DifferentInjector()
        {
            var altInjector = new AlternateDummyInjector();
            FragmentArgs.autoMappingInjector = altInjector;

            int testTarget = 2024;
            FragmentArgs.Inject(testTarget);
            Assert.True(altInjector.Invoked);

            FragmentArgs.autoMappingInjector = null;
        }
    }
}