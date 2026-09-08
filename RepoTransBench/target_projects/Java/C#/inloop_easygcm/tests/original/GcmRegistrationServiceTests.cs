using Xunit;
using Moq;
using easygcm;

namespace tests.original
{
    public class GcmRegistrationServiceTests
    {
        private Mock<object> mockContext;

        public GcmRegistrationServiceTests()
        {
            mockContext = new Mock<object>();
        }

        [Fact]
        public void TestCreateGcmRegistrationIntent_Defaults()
        {
            var intent = GcmRegistrationService.CreateGcmRegistrationIntent(mockContext.Object);
            Assert.NotNull(intent);
            Assert.Equal(GcmRegistrationService.ACTION_REGISTER_GCM, intent.GetIntExtra(GcmRegistrationService.EXTRA_ACTION_CODE, -1));
        }

        [Fact]
        public void TestCreateGcmRegistrationIntent_WithWakeLock()
        {
            var intent = GcmRegistrationService.CreateGcmRegistrationIntent(mockContext.Object, true);
            Assert.True(intent.GetBooleanExtra(GcmRegistrationService.EXTRA_HAS_WAKELOCK, false));
        }

        [Fact]
        public void TestOnHandleIntent_AlreadyRegistered()
        {
            var intent = GcmRegistrationService.CreateGcmRegistrationIntent(mockContext.Object);
            var service = new GcmRegistrationServiceTestDouble() { IsRegistered = true };
            service.OnHandleIntent(intent);
            Assert.True(service.ReleaseWakeLockCalled);
            Assert.False(service.RegisterGcmCalled);
        }

        [Fact]
        public void TestOnHandleIntent_RegistersAndHandlesError()
        {
            var intent = GcmRegistrationService.CreateGcmRegistrationIntent(mockContext.Object);
            var service = new GcmRegistrationServiceTestDouble() { IsRegistered = false };
            service.OnHandleIntent(intent);
            Assert.True(service.ReleaseWakeLockCalled);
            Assert.True(service.RegisterGcmCalled);
        }
    }

    public class GcmRegistrationServiceTestDouble : GcmRegistrationService
    {
        public bool IsRegistered = false;
        public bool RegisterGcmCalled = false;
        public bool ReleaseWakeLockCalled = false;

        protected override bool IsAlreadyRegistered(object context)
        {
            return IsRegistered;
        }

        protected override void RegisterGcm()
        {
            RegisterGcmCalled = true;
        }

        protected override void ReleaseWakeLock()
        {
            ReleaseWakeLockCalled = true;
        }
    }
}