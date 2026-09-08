using Xunit;

namespace ComponentDemo.PublicTests
{
    // Import/duplicate definitions if not referenced
    public interface IAccountService
    {
        bool IsLogin();
        string GetAccountId();
        object NewUserFragment(object activity, int containerId, object manager, object bundle, string tag);
    }

    public class EmptyAccountService : IAccountService
    {
        public bool IsLogin() => false;
        public string GetAccountId() => "";
        public object NewUserFragment(object activity, int containerId, object manager, object bundle, string tag) => null;
    }

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

        public static void Reset()
        {
            _instance = null;
        }
    }

    public class ServiceFactoryPublicTest : System.IDisposable
    {
        public ServiceFactoryPublicTest()
        {
            ServiceFactory.Reset();
        }

        public void Dispose()
        {
            ServiceFactory.Reset();
        }

        class DifferentMockAccountService : IAccountService
        {
            public bool IsLogin() => false;
            public string GetAccountId() => "public_mock_id";
            public object NewUserFragment(object activity, int containerId, object manager, object bundle, string tag) => null;
        }

        [Fact]
        public void TestSingletonInstancePublic()
        {
            var instance1 = ServiceFactory.GetInstance();
            var instance2 = ServiceFactory.GetInstance();
            Assert.Same(instance1, instance2);
        }

        [Fact]
        public void TestSetAndGetDifferentMockAccountService()
        {
            var service = new DifferentMockAccountService();
            ServiceFactory.GetInstance().SetAccountService(service);
            var result = ServiceFactory.GetInstance().GetAccountService();
            Assert.Same(service, result);
        }

        [Fact]
        public void TestGetAccountServiceReturnsEmptyIfNullPublic()
        {
            ServiceFactory.GetInstance().SetAccountService(null);
            var service = ServiceFactory.GetInstance().GetAccountService();
            Assert.NotNull(service);
            Assert.IsType<EmptyAccountService>(service);
        }
    }
}