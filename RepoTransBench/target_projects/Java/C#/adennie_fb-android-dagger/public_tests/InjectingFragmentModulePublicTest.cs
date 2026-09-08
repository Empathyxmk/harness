using Moq;
using Xunit;
using ProjectName;

namespace PublicTests
{
    public class InjectingFragmentModulePublicTest
    {
        private Mock<SupportV4Fragment> _mockSupportV4FragmentA;
        private Mock<SupportV4Fragment> _mockSupportV4FragmentB;
        private Mock<AppFragment> _mockFragmentA;
        private Mock<AppFragment> _mockFragmentB;
        private Mock<Injector> _mockInjectorA;
        private Mock<Injector> _mockInjectorB;

        private InjectingFragmentModule _moduleA;
        private InjectingFragmentModule _moduleB;

        public InjectingFragmentModulePublicTest()
        {
            _mockSupportV4FragmentA = new Mock<SupportV4Fragment>();
            _mockSupportV4FragmentB = new Mock<SupportV4Fragment>();
            _mockFragmentA = new Mock<AppFragment>();
            _mockFragmentB = new Mock<AppFragment>();
            _mockInjectorA = new Mock<Injector>();
            _mockInjectorB = new Mock<Injector>();

            _moduleA = new InjectingFragmentModule(_mockSupportV4FragmentA.Object, _mockInjectorA.Object);
            _moduleB = new InjectingFragmentModule(_mockFragmentB.Object, _mockInjectorB.Object);
        }

        [Fact]
        public void TestSupportV4FragmentConstructorAndProviderPublic()
        {
            var providedFragment = _moduleA.ProvideSupportV4Fragment();
            Assert.NotNull(providedFragment);
            Assert.Equal(_mockSupportV4FragmentA.Object, providedFragment);
        }

        [Fact]
        public void TestAppFragmentConstructorAndProviderPublic()
        {
            var providedFragment = _moduleB.ProvideFragment();
            Assert.NotNull(providedFragment);
            Assert.Equal(_mockFragmentB.Object, providedFragment);
        }

        [Fact]
        public void TestProvideFragmentInjectorForSupportV4Public()
        {
            var providedInjector = _moduleA.ProvideFragmentInjector();
            Assert.NotNull(providedInjector);
            Assert.Equal(_mockInjectorA.Object, providedInjector);
        }

        [Fact]
        public void TestProvideFragmentInjectorForAppFragmentPublic()
        {
            var providedInjector = _moduleB.ProvideFragmentInjector();
            Assert.NotNull(providedInjector);
            Assert.Equal(_mockInjectorB.Object, providedInjector);
        }
    }
}