using System;
using System.Collections.Generic;
using System.Security.Principal;
using Xunit;
using Moq;
using Demo;

namespace Demo.PublicTests
{
    public class SsoApplicationPublicTest
    {
        [Fact]
        public void TestDashboardMessage_Public()
        {
            var app = new SsoApplication();
            var message = app.Dashboard();
            Assert.NotNull(message);
            Assert.True(message.ContainsKey("message"));
            Assert.IsType<string>(message["message"]);
        }

        [Fact]
        public void TestUserPrincipal_Public()
        {
            var app = new SsoApplication();
            var principal = new GenericPrincipal(new GenericIdentity("publicuser"), null);
            var returned = app.User(principal) as IPrincipal;
            Assert.Equal(principal.Identity.Name, returned.Identity.Name);
            Assert.Equal("publicuser", returned.Identity.Name);

            var specialPrincipal = new GenericPrincipal(new GenericIdentity("用户123"), null);
            var specialReturned = app.User(specialPrincipal) as IPrincipal;
            Assert.Equal("用户123", specialReturned.Identity.Name);
        }

        [Fact]
        public void TestMainWithArgs_Public()
        {
            SsoApplication.Main(new string[] { "--fakeArg=1" });
        }

        [Fact]
        public void TestLoginErrorsDashboard_Public()
        {
            var errors = new SsoApplication.LoginErrors();
            var result = errors.Dashboard();
            Assert.StartsWith("redirect:/#", result);
            Assert.Contains("/", result);
            Assert.Equal("redirect:/#/", result);
        }

        [Fact]
        public void TestCsrfHeaderFilterSetsCookie_Public()
        {
            var configurer = new SsoApplication.LoginConfigurer();

            var request = new Mock<ITestHttpServletRequest>();
            var response = new Mock<ITestHttpServletResponse>();
            var chain = new Mock<ITestFilterChain>();

            var csrfToken = new Mock<ITestCsrfToken>();
            csrfToken.Setup(x => x.Token).Returns("publicTokenXYZ");
            request.Setup(x => x.GetAttribute("CsrfToken")).Returns(csrfToken.Object);

            var filterObj = configurer.CsrfHeaderFilter();
            Assert.NotNull(filterObj);
            var filter = (Demo.Tests.CsrfHeaderFilterFake)filterObj;
            filter.DoFilter(request.Object, response.Object, chain.Object);

            // Ensure cookie added with proper name & value
            response.Verify(x => x.AddCookie(It.Is<Demo.Tests.ITestCookie>(c => c.Name == "XSRF-TOKEN" && c.Value == "publicTokenXYZ")), Times.Once);
            chain.Verify(x => x.DoFilter(request.Object, response.Object), Times.Once);
        }

        [Fact]
        public void TestCsrfHeaderFilterNoCsrf_Public()
        {
            var configurer = new SsoApplication.LoginConfigurer();

            var request = new Mock<ITestHttpServletRequest>();
            var response = new Mock<ITestHttpServletResponse>();
            var chain = new Mock<ITestFilterChain>();

            request.Setup(x => x.GetAttribute("CsrfToken")).Returns((ITestCsrfToken)null);

            var filterObj = configurer.CsrfHeaderFilter();
            var filter = (Demo.Tests.CsrfHeaderFilterFake)filterObj;
            filter.DoFilter(request.Object, response.Object, chain.Object);

            response.Verify(x => x.AddCookie(It.IsAny<Demo.Tests.ITestCookie>()), Times.Never);
            chain.Verify(x => x.DoFilter(request.Object, response.Object), Times.Once);
        }

        [Fact]
        public void TestCsrfTokenRepository_Public()
        {
            var configurer = new SsoApplication.LoginConfigurer();
            var repository = configurer.CsrfTokenRepository();
            Assert.NotNull(repository);

            var headerNameField = repository.GetType().GetField("headerName");
            Assert.NotNull(headerNameField);
            var value = headerNameField.GetValue(repository);
            Assert.IsType<string>(value);
            Assert.Equal("X-XSRF-TOKEN", value);
        }
    }

    // Interfaces for mocks (re-use with test implementation)
    public interface ITestHttpServletRequest
    {
        object GetAttribute(string name);
    }
    public interface ITestHttpServletResponse
    {
        void AddCookie(Demo.Tests.ITestCookie cookie);
    }
    public interface ITestFilterChain
    {
        void DoFilter(object request, object response);
    }
    public interface ITestCsrfToken
    {
        string Token { get; }
    }
}