using Xunit;
using easygcm;
using System.Collections.Generic;

namespace tests.original
{
    public class EasyGcmListenerServiceTests
    {
        public class EasyGcmStubber : GcmListener
        {
            public static bool CalledOnMessage = false;
            public void OnMessage(string from, IDictionary<string, object> data)
            {
                CalledOnMessage = true;
            }
        }

        [Fact]
        public void TestOnMessageReceived_DelegatesToEasyGcm()
        {
            var stubber = new EasyGcmStubber();
            EasyGcm.GetInstance().SetGcmListener(stubber);

            var data = new Dictionary<string, object> { { "key", "value" } };
            var service = new EasyGcmListenerService();
            service.OnMessageReceived("sender", data);
            Assert.True(EasyGcmStubber.CalledOnMessage);
            EasyGcmStubber.CalledOnMessage = false;
        }
    }

    public class EasyGcmListenerService
    {
        public void OnMessageReceived(string from, IDictionary<string, object> data)
        {
            var listener = EasyGcm.GetInstance().GetGcmListener(null);
            listener?.OnMessage(from, data);
        }
    }
}