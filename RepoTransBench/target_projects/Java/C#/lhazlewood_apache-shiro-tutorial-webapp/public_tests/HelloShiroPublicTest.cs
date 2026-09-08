using System;
using Xunit;
using HelloShiroProject;

namespace PublicTests
{
    public class HelloShiroPublicTest
    {
        private HelloShiro shiro;

        public HelloShiroPublicTest()
        {
            shiro = new HelloShiro();
        }

        [Fact]
        public void TestLoginSuccess_Public()
        {
            // Since only "admin"/"adminpass" is valid, test with a similar logic but change string casing to check strict equality
            // Try "Admin"/"Adminpass" (should fail: case sensitive)
            Assert.False(shiro.login("Admin", "Adminpass"));
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());

            // Now test: use leading/trailing whitespace (should also fail)
            Assert.False(shiro.login(" admin ", " adminpass "));
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());
        }

        [Fact]
        public void TestLoginFailure_EmptyFields()
        {
            // Try empty username
            Assert.False(shiro.login("", "adminpass"));
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());

            // Try empty password
            Assert.False(shiro.login("admin", ""));
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());
        }

        [Fact]
        public void TestLoginFailure_NullFields()
        {
            // Try null username (should handle gracefully)
            Assert.False(shiro.login(null, "adminpass"));
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());

            // Try null password
            Assert.False(shiro.login("admin", null));
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());
        }

        [Fact]
        public void TestLogoutAfterFailedLogin()
        {
            Assert.False(shiro.login("nope", "nope"));
            shiro.logout();
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());
        }

        [Fact]
        public void TestWelcomeMessage_AdminAfterManualSet()
        {
            // Use internal setters to mimic reflection, set user = "Admin" (not "admin")
            shiro.SetAuthenticated(true);
            shiro.SetUser("Admin");
            Assert.Equal("Welcome, Admin!", shiro.getWelcomeMessage());
        }

        [Fact]
        public void TestMultipleLoginLogoutDifferentUsernames()
        {
            // Fails with username = "root" (not admin)
            Assert.False(shiro.login("root", "supersecret"));
            shiro.logout();
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());

            // Fails with username = "user"
            Assert.False(shiro.login("user", "userpass"));
            Assert.False(shiro.isAuthenticated());
            Assert.Null(shiro.getUser());
            Assert.Equal("Please log in.", shiro.getWelcomeMessage());

            // Now authenticate and check values
            Assert.True(shiro.login("admin", "adminpass"));
            Assert.True(shiro.isAuthenticated());
            Assert.Equal("admin", shiro.getUser());
            Assert.Equal("Welcome, admin!", shiro.getWelcomeMessage());
        }
    }
}