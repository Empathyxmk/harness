using Xunit;

namespace ComponentDemo.Tests.Original
{
    public class EmptyAccountServiceTest
    {
        // The EmptyAccountService definition is imported from ServiceFactoryTest

        [Fact]
        public void TestIsLoginIsFalse()
        {
            var service = new ComponentDemo.Tests.Original.EmptyAccountService();
            Assert.False(service.IsLogin());
        }

        [Fact]
        public void TestGetAccountIdIsNull()
        {
            var service = new ComponentDemo.Tests.Original.EmptyAccountService();
            Assert.Null(service.GetAccountId());
        }

        [Fact]
        public void TestNewUserFragmentIsNull()
        {
            var service = new ComponentDemo.Tests.Original.EmptyAccountService();
            Assert.Null(service.NewUserFragment(null, 0, null, null, null));
        }
    }
}