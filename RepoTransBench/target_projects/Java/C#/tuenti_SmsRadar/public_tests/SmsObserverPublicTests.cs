using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Public
{
    public class SmsObserverPublicTests
    {
        [Fact]
        public void TestOnSmsReceivedCallbackDiffData()
        {
            bool trigger = false;
            SmsListener listener = new TestSmsListener((sms) =>
            {
                Assert.Equal("ObserverName", sms.GetContact());
                Assert.Equal("+999999999", sms.GetAddress());
                Assert.Equal("ObserverMsg", sms.GetMessage());
                trigger = true;
            });

            var smsObj = new Sms("ObserverName", "+999999999", "ObserverMsg", 1987654321L, SmsType.SENT);
            listener.OnSmsReceived(smsObj);
            Assert.True(trigger);
        }

        private class TestSmsListener : SmsListener
        {
            private readonly System.Action<Sms> _onReceived;

            public TestSmsListener(System.Action<Sms> onReceived)
            {
                _onReceived = onReceived;
            }

            public void OnSmsReceived(Sms sms)
            {
                _onReceived?.Invoke(sms);
            }

            public void OnSmsSent(Sms sms)
            {
                // Not needed for this test.
            }
        }
    }
}