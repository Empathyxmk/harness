using Xunit;
using Moq;
using easygcm;

namespace public_tests
{
    public class GcmHelperPublicTests
    {
        private Mock<object> mockContext;

        public GcmHelperPublicTests()
        {
            mockContext = new Mock<object>();
        }

        [Fact]
        public void TestInitDelegatesToEasyGcmPublic()
        {
            GcmHelper.Init(mockContext.Object);
        }

        [Fact]
        public void TestSetGcmListenerPublic()
        {
            var mockListener = new Mock<GcmListener>().Object;
            GcmHelper.SetGcmListener(mockListener);
        }

        [Fact]
        public void TestSetCheckServicesHandlerPublic()
        {
            var mockHandler = new Mock<GcmServicesHandler>().Object;
            GcmHelper.SetCheckServicesHandler(mockHandler);
        }

        [Fact]
        public void TestIsRegisteredPublicDifferentInput()
        {
            GcmHelper.IsRegistered(mockContext.Object);
        }

        [Fact]
        public void TestGetRegistrationIdPublicDifferentInput()
        {
            GcmHelper.GetRegistrationId(mockContext.Object);
        }

        [Fact]
        public void TestRemoveRegistrationIdPublicDifferentInput()
        {
            GcmHelper.RemoveRegistrationId(mockContext.Object);
        }

        [Fact]
        public void TestGetGcmSenderIdPublicDifferentInput()
        {
            GcmHelper.GetGcmSenderId(mockContext.Object);
        }

        [Fact]
        public void TestSetLoggingEnabledPublic()
        {
            var helper = GcmHelper.GetInstance();
            helper.SetLoggingEnabled(5);
        }

        [Fact]
        public void TestGetGcmListenerPublic()
        {
            var helper = GcmHelper.GetInstance();
            helper.GetGcmListener(mockContext.Object);
        }
    }
}