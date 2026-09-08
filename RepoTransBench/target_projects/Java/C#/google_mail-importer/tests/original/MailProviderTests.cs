using System;
using System.Net.Mail;
using Xunit;
using Moq;
using System.Threading.Tasks;

namespace GoogleMailImporter.Tests.Original
{
    public class MailProviderTests
    {
        private class DummyMailProvider : IMailProvider<string>
        {
            private readonly bool _throwException;
            public DummyMailProvider(bool throwException)
            {
                _throwException = throwException;
            }
            public string Get()
            {
                if (_throwException)
                    throw new SmtpException("fail");
                return "success";
            }
        }

        [Fact]
        public void TestGetSuccess()
        {
            IMailProvider<string> mailProvider = new DummyMailProvider(false);
            Assert.Equal("success", mailProvider.Get());
        }

        [Fact]
        public void TestGetThrowsException()
        {
            IMailProvider<string> mailProvider = new DummyMailProvider(true);
            Assert.Throws<SmtpException>(() => mailProvider.Get());
        }
    }

    // Interface extracted to fit C#.
    public interface IMailProvider<T>
    {
        T Get();
    }
}