using Xunit;
using Moq;
using easygcm;

namespace tests.original
{
    public class NetworkStateReceiverTests
    {
        private Mock<object> mockContext;
        private Mock<object> mockIntent;

        public NetworkStateReceiverTests()
        {
            mockContext = new Mock<object>();
            mockIntent = new Mock<object>();
        }

        [Fact]
        public void TestReceive_RegistersWhenAllowed()
        {
            GcmUtils.forcedResult = true;
            GcmUtils.overrideCall = true;
            var networkReceiver = new NetworkStateReceiverTestDouble();
            var regIntent = new GcmRegistrationService.Intent();
            var called = false;
            networkReceiver.OnStartWakefulService = (ctx, intent) =>
            {
                called = true;
                Assert.Equal(regIntent, intent);
            };
            NetworkStateReceiverTestDouble.SetRegistrationIntent(regIntent);
            networkReceiver.OnReceive(mockContext.Object, mockIntent.Object);
            Assert.True(called);
            GcmUtils.overrideCall = false;
            GcmUtils.forcedResult = false;
            NetworkStateReceiverTestDouble.Reset();
        }

        [Fact]
        public void TestReceive_DoesNothingIfNotAllowed()
        {
            GcmUtils.forcedResult = false;
            GcmUtils.overrideCall = true;
            var networkReceiver = new NetworkStateReceiverTestDouble();
            bool called = false;
            networkReceiver.OnStartWakefulService = (ctx, intent) => { called = true; };
            networkReceiver.OnReceive(mockContext.Object, mockIntent.Object);
            Assert.False(called);
            GcmUtils.overrideCall = false;
            GcmUtils.forcedResult = false;
            NetworkStateReceiverTestDouble.Reset();
        }
    }

    public class NetworkStateReceiverTestDouble : NetworkStateReceiver
    {
        public static GcmRegistrationService.Intent RegistrationIntent = null;
        public System.Action<object, object> OnStartWakefulService = null;

        public override void StartWakefulService(object context, object intent)
        {
            OnStartWakefulService?.Invoke(context, intent);
        }

        public override void OnReceive(object context, object intent)
        {
            base.OnReceive(context, intent);
        }

        public static void SetRegistrationIntent(GcmRegistrationService.Intent intent)
        {
            RegistrationIntent = intent;
        }

        public static void Reset()
        {
            RegistrationIntent = null;
        }
    }
}