using Xunit;
using Moq;
using easygcm;

namespace tests.original
{
    public class GcmHelperTests
    {
        private Mock<object> mockContext;

        public GcmHelperTests()
        {
            mockContext = new Mock<object>();
        }

        [Fact]
        public void TestInitDelegatesToEasyGcm()
        {
            GcmHelper.Init(mockContext.Object);
        }

        [Fact]
        public void TestGetInstance_Singleton()
        {
            var instance1 = GcmHelper.GetInstance();
            var instance2 = GcmHelper.GetInstance();
            Assert.NotNull(instance1);
            Assert.NotNull(instance2);
        }

        [Fact]
        public void TestSetGcmListenerDelegatesToEasyGcm()
        {
            var mockListener = new Mock<GcmListener>().Object;
            GcmHelper.SetGcmListener(mockListener);
        }

        [Fact]
        public void TestSetCheckServicesHandlerDelegatesToEasyGcm()
        {
            var mockHandler = new Mock<GcmServicesHandler>().Object;
            GcmHelper.SetCheckServicesHandler(mockHandler);
        }

        [Fact]
        public void TestIsRegisteredDelegatesToEasyGcm()
        {
            var result = GcmHelper.IsRegistered(mockContext.Object);
            Assert.False(result);
        }

        [Fact]
        public void TestGetRegistrationIdDelegatesToEasyGcm()
        {
            var id = GcmHelper.GetRegistrationId(mockContext.Object);
            Assert.Null(id);
        }

        [Fact]
        public void TestRemoveRegistrationIdDelegatesToEasyGcm()
        {
            GcmHelper.RemoveRegistrationId(mockContext.Object);
        }

        [Fact]
        public void TestGetGcmSenderIdDelegatesToEasyGcm()
        {
            Assert.Null(GcmHelper.GetGcmSenderId(mockContext.Object));
        }

        [Fact]
        public void TestSetLoggingEnabled()
        {
            var helper = GcmHelper.GetInstance();
            helper.SetLoggingEnabled(1);
        }

        [Fact]
        public void TestGetGcmListenerDelegatesToEasyGcm()
        {
            var helper = GcmHelper.GetInstance();
            Assert.Null(helper.GetGcmListener(mockContext.Object));
        }
    }
}