using System;
using Xunit;
using HelloShiroProject;

namespace OriginalTests
{
    public class HelloShiroTest
    {
        private HelloShiro shiro;

        public HelloShiroTest()
        {
            shiro = new HelloShiro();
        }

        [Fact]
        public void TestLoginSuccess()
        {
            Assert.True(shiro.login("admin", "adminpass"));
            Assert.True(shiro.isAuthenticated());
            Assert.Equal("admin", shiro.getUser());
            Assert.Equal("Welcome, admin!", shiro.getWelcomeMessage());
        }

        [Fact]
        public void TestLoginFailure_BadPassword()
        {
            Assert.False(shiro.login("admin", "wrongpass"));
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());
        }

        [Fact]
        public void TestLoginFailure_UnknownUser()
        {
            Assert.False(shiro.login("bob", "somepass"));
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());
        }

        [Fact]
        public void TestLogout()
        {
            shiro.login("admin", "adminpass");
            shiro.logout();
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());
        }

        [Fact]
        public void TestWelcomeMessageNotAuthenticated()
        {
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());
        }

        [Fact]
        public void TestWelcomeMessageUnknownUser()
        {
            // Equivalent of Java reflection: use internal setter, since only admin can login
            shiro.SetAuthenticated(true);
            shiro.SetUser("otheruser");
            Assert.Equal("Welcome, otheruser!", shiro.getWelcomeMessage());
        }

        [Fact]
        public void TestMultipleLoginLogoutCycles()
        {
            Assert.True(shiro.login("admin", "adminpass"));
            shiro.logout();
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());

            Assert.False(shiro.login("test", "bad"));
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());

            Assert.True(shiro.login("admin", "adminpass"));
            Assert.True(shiro.isAuthenticated());
            Assert.Equal("admin", shiro.getUser());
        }
    }
}