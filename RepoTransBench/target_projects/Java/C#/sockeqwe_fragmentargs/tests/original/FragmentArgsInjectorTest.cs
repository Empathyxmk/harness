using Xunit;

namespace ProjectName.Tests.Original
{
    public class FragmentArgsInjectorTest
    {
        public interface IFragmentArgsInjector
        {
            void Inject(object target);
        }

        [Fact]
        public void InjectorInterfaceShouldAllowAnyObject()
        {
            IFragmentArgsInjector inj = new DummyInjector();
            inj.Inject("dummy");
        }

        private class DummyInjector : IFragmentArgsInjector
        {
            public void Inject(object target)
            {
                // no-op
            }
        }
    }
}