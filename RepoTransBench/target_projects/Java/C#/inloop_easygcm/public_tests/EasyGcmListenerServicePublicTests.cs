using Xunit;
using easygcm;
using System.Collections.Generic;

namespace public_tests
{
    public class EasyGcmListenerServicePublicTests
    {
        public class EasyGcmStubberPublic : GcmListener
        {
            public static bool CalledOnMessage = false;
            public void OnMessage(string from, IDictionary<string, object> data)
            {
                if (from == "public_sender" && data.ContainsKey("another_key") && (string)data["another_key"] == "another_value")
                {
                    CalledOnMessage = true;
                }
            }
        }

        [Fact]
        public void TestOnMessageReceived_DelegatesToEasyGcm_Different()
        {
            var stubber = new EasyGcmStubberPublic();
            EasyGcm.GetInstance().SetGcmListener(stubber);

            var data = new Dictionary<string, object> { { "another_key", "another_value" } };
            var service = new EasyGcmListenerServicePublic();
            service.OnMessageReceived("public_sender", data);
            Assert.True(EasyGcmStubberPublic.CalledOnMessage);
            EasyGcmStubberPublic.CalledOnMessage = false;
        }
    }

    public class EasyGcmListenerServicePublic
    {
        public void OnMessageReceived(string from, IDictionary<string, object> data)
        {
            var listener = EasyGcm.GetInstance().GetGcmListener(null);
            listener?.OnMessage(from, data);
        }
    }
}