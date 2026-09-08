using Xunit;

namespace ComponentDemo.Tests.Original
{
    // Simulate the IAccountService contract as per test requirements
    public interface IAccountService
    {
        bool IsLogin();
        string GetAccountId();
        object NewUserFragment(object activity, int containerId, object manager, object bundle, string tag);
    }

    // Simulate the EmptyAccountService as in the Java code
    public class EmptyAccountService : IAccountService
    {
        public bool IsLogin() => false;
        public string GetAccountId() => null;
        public object NewUserFragment(object activity, int containerId, object manager, object bundle, string tag) => null;
    }

    // Singleton as used in tests
    public class ServiceFactory
    {
        private static ServiceFactory _instance;
        private IAccountService _accountService;

        private ServiceFactory() { }

        public static ServiceFactory GetInstance()
        {
            if (_instance == null)
                _instance = new ServiceFactory();
            return _instance;
        }

        public void SetAccountService(IAccountService service)
        {
            _accountService = service;
        }

        public IAccountService GetAccountService()
        {
            if (_accountService == null)
                return new EmptyAccountService();
            return _accountService;
        }

        // Test support: reset factory for test independence
        public static void Reset()
        {
            _instance = null;
        }
    }

    public class ServiceFactoryTest : System.IDisposable
    {
        public ServiceFactoryTest()
        {
            // Ensure test isolation
            ServiceFactory.Reset();
        }

        public void Dispose()
        {
            ServiceFactory.Reset();
        }

        class MockAccountService : IAccountService
        {
            public bool IsLogin() => true;
            public string GetAccountId() => "mock";
            public object NewUserFragment(object activity, int containerId, object manager, object bundle, string tag) => null;
        }

        [Fact]
        public void TestSingletonInstance()
        {
            var factory1 = ServiceFactory.GetInstance();
            var factory2 = ServiceFactory.GetInstance();
            Assert.Same(factory1, factory2);
        }

        [Fact]
        public void TestSetAndGetAccountService()
        {
            var mockService = new MockAccountService();
            ServiceFactory.GetInstance().SetAccountService(mockService);
            var result = ServiceFactory.GetInstance().GetAccountService();
            Assert.Same(mockService, result);
        }

        [Fact]
        public void TestGetAccountServiceReturnsEmptyIfNull()
        {
            ServiceFactory.GetInstance().SetAccountService(null);
            var service = ServiceFactory.GetInstance().GetAccountService();
            Assert.NotNull(service);
            Assert.IsType<EmptyAccountService>(service);
        }
    }
}