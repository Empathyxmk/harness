using Xunit;

namespace ProjectName.PublicTests
{
    public class FragmentArgsInjectorPublicTest
    {
        public interface IFragmentArgsInjector
        {
            void Inject(object target);
        }

        private class DummyInjector : IFragmentArgsInjector
        {
            public void Inject(object target)
            {
                // still accepts any target, use different type
                if (target is double)
                {
                    // no-op
                }
            }
        }

        [Fact]
        public void InjectorInterfaceShouldAllowAnyObject_PublicTest()
        {
            IFragmentArgsInjector inj = new DummyInjector();
            inj.Inject(77.7); // pass a double, different from original test
        }
    }
}