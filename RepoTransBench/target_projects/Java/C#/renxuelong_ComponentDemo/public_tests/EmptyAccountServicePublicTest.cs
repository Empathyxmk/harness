using Xunit;

namespace ComponentDemo.PublicTests
{
    public class EmptyAccountServicePublicTest
    {
        public class EmptyAccountService
        {
            public bool IsLogin() => false;
            public string GetAccountId() => "";
        }

        [Fact]
        public void TestIsLoginDifferent()
        {
            var s = new EmptyAccountService();
            Assert.False(s.IsLogin());
        }

        [Fact]
        public void TestGetAccountIdReturnsEmptyStringPublic()
        {
            var s = new EmptyAccountService();
            Assert.Equal("", s.GetAccountId());
        }
    }
}