using Moq;
using Xunit;
using ProjectName;

namespace OriginalTests
{
    public class InjectingFragmentModuleTest
    {
        private Mock<SupportV4Fragment> _mockSupportV4Fragment;
        private Mock<AppFragment> _mockFragment;
        private Mock<Injector> _mockInjector;

        private InjectingFragmentModule _supportV4Module;
        private InjectingFragmentModule _appFragmentModule;

        public InjectingFragmentModuleTest()
        {
            _mockSupportV4Fragment = new Mock<SupportV4Fragment>();
            _mockFragment = new Mock<AppFragment>();
            _mockInjector = new Mock<Injector>();

            _supportV4Module = new InjectingFragmentModule(_mockSupportV4Fragment.Object, _mockInjector.Object);
            _appFragmentModule = new InjectingFragmentModule(_mockFragment.Object, _mockInjector.Object);
        }

        [Fact]
        public void TestSupportV4FragmentConstructorAndProvider()
        {
            var providedFragment = _supportV4Module.ProvideSupportV4Fragment();
            Assert.NotNull(providedFragment);
            Assert.Equal(_mockSupportV4Fragment.Object, providedFragment);
        }

        [Fact]
        public void TestAppFragmentConstructorAndProvider()
        {
            var providedFragment = _appFragmentModule.ProvideFragment();
            Assert.NotNull(providedFragment);
            Assert.Equal(_mockFragment.Object, providedFragment);
        }

        [Fact]
        public void TestProvideFragmentInjectorForSupportV4()
        {
            var providedInjector = _supportV4Module.ProvideFragmentInjector();
            Assert.NotNull(providedInjector);
            Assert.Equal(_mockInjector.Object, providedInjector);
        }

        [Fact]
        public void TestProvideFragmentInjectorForAppFragment()
        {
            var providedInjector = _appFragmentModule.ProvideFragmentInjector();
            Assert.NotNull(providedInjector);
            Assert.Equal(_mockInjector.Object, providedInjector);
        }
    }
}