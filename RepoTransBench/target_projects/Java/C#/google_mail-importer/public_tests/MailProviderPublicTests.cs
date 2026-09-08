using System.Net.Mail;
using Xunit;

namespace GoogleMailImporter.PublicTests
{
    public class MailProviderPublicTests
    {
        private class AnotherDummyMailProvider : IMailProvider<int>
        {
            private readonly bool _shouldThrow;
            public AnotherDummyMailProvider(bool shouldThrow) { _shouldThrow = shouldThrow; }
            public int Get()
            {
                if (_shouldThrow)
                    throw new SmtpException("provider fail");
                return 12345;
            }
        }

        [Fact]
        public void TestGetDifferentSuccess()
        {
            IMailProvider<int> mailProvider = new AnotherDummyMailProvider(false);
            Assert.Equal(12345, mailProvider.Get());
        }

        [Fact]
        public void TestGetThrowsMessagingExceptionPublic()
        {
            IMailProvider<int> mailProvider = new AnotherDummyMailProvider(true);
            Assert.Throws<SmtpException>(() => mailProvider.Get());
        }
    }

    public interface IMailProvider<T>
    {
        T Get();
    }
}