using System.Collections.Generic;
using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Original
{
    public class SmsStorageTests
    {
        private class DummySmsStorage : ISmsStorage
        {
            private int _last = -1;
            private bool _first = true;

            public void UpdateLastSmsIntercepted(int smsId)
            {
                _last = smsId;
                _first = false;
            }

            public int GetLastSmsIntercepted()
            {
                return _last;
            }

            public bool IsFirstSmsIntercepted()
            {
                return _first;
            }
        }

        private DummySmsStorage _storage;

        public SmsStorageTests()
        {
            _storage = new DummySmsStorage();
        }

        [Fact]
        public void TestIsFirstSmsInterceptedInitiallyTrue()
        {
            Assert.True(_storage.IsFirstSmsIntercepted());
        }

        [Fact]
        public void TestUpdateAndGetLastSms()
        {
            _storage.UpdateLastSmsIntercepted(42);
            Assert.False(_storage.IsFirstSmsIntercepted());
            Assert.Equal(42, _storage.GetLastSmsIntercepted());
        }

        [Fact]
        public void TestAddAndGetAllSms()
        {
            var storage = new SmsStorage();
            var sms1 = new Sms("1", "111", "msg1", SmsType.RECEIVED);
            var sms2 = new Sms("2", "222", "msg2", SmsType.SENT);
            storage.AddSms(sms1);
            storage.AddSms(sms2);

            var all = storage.GetAllSms();
            Assert.Equal(2, all.Count);
            Assert.Contains(sms1, all);
            Assert.Contains(sms2, all);
        }

        [Fact]
        public void TestClear()
        {
            var storage = new SmsStorage();
            storage.AddSms(new Sms("1", "111", "msg1", SmsType.RECEIVED));
            storage.Clear();
            Assert.Empty(storage.GetAllSms());
        }
    }
}