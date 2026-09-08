using System;
using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Original
{
    public class SharedPreferencesSmsStorageTests
    {
        private const int DefaultValue = -1;
        private const int AnySmsId = 1;

        private SharedPreferencesSmsStorage _smsStorage;

        public SharedPreferencesSmsStorageTests()
        {
            _smsStorage = new SharedPreferencesSmsStorage();
            _smsStorage.ClearPreferences();
        }

        [Fact]
        public void ShouldReturnDefaultValueIfHadNotBeenEditedPreviously()
        {
            Assert.Equal(DefaultValue, _smsStorage.GetLastSmsIntercepted());
        }

        [Fact]
        public void ShouldUpdateLastSmsInterceptedId()
        {
            _smsStorage.UpdateLastSmsIntercepted(AnySmsId);
            Assert.Equal(AnySmsId, _smsStorage.GetLastSmsIntercepted());
        }

        [Fact]
        public void ShouldReturnTrueIfIsTheFirstSmsIntercepted()
        {
            Assert.True(_smsStorage.IsFirstSmsIntercepted());
        }
    }
}