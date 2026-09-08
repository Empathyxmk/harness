using System;
using System.Collections.Generic;
using System.Security.Principal;
using Xunit;
using Moq;
using Demo;

namespace Demo.Tests
{
    public class SsoApplicationTest
    {
        [Fact]
        public void TestDashboardMessage()
        {
            var app = new SsoApplication();
            var message = app.Dashboard();
            Assert.NotNull(message);
            Assert.True(message.ContainsKey("message"));
            Assert.Equal("Yay!", message["message"]);
        }

        [Fact]
        public void TestUserPrincipal()
        {
            var app = new SsoApplication();
            var principal = new GenericPrincipal(new GenericIdentity("testuser"), null);
            Assert.Equal(principal.Identity.Name, ((IPrincipal)app.User(principal)).Identity.Name);
            Assert.Equal("testuser", ((IPrincipal)app.User(principal)).Identity.Name);
        }

        [Fact]
        public void TestMainNoArgs()
        {
            SsoApplication.Main(new string[] { });
        }

        [Fact]
        public void TestLoginErrorsDashboard()
        {
            var errors = new SsoApplication.LoginErrors();
            Assert.Equal("redirect:/#/", errors.Dashboard());
        }

        [Fact]
        public void TestCsrfHeaderFilterSetsCookie()
        {
            var configurer = new SsoApplication.LoginConfigurer();

            // mocks for Filter, request, response, chain
            var request = new Mock<ITestHttpServletRequest>();
            var response = new Mock<ITestHttpServletResponse>();
            var chain = new Mock<ITestFilterChain>();

            // simulate csrf token
            var csrfToken = new Mock<ITestCsrfToken>();
            csrfToken.Setup(x => x.Token).Returns("testToken");
            request.Setup(x => x.GetAttribute("CsrfToken")).Returns(csrfToken.Object);

            // access the filter via method
            var filterObj = configurer.CsrfHeaderFilter();
            Assert.NotNull(filterObj);
            var filter = (CsrfHeaderFilterFake)filterObj;
            // Simulate calling doFilter
            filter.DoFilter(request.Object, response.Object, chain.Object);
            // Verify that addCookie was called
            response.Verify(x => x.AddCookie(It.IsAny<ITestCookie>()), Times.Once);
            chain.Verify(x => x.DoFilter(request.Object, response.Object), Times.Once);
        }

        [Fact]
        public void TestCsrfHeaderFilterNoCsrf()
        {
            var configurer = new SsoApplication.LoginConfigurer();

            var request = new Mock<ITestHttpServletRequest>();
            var response = new Mock<ITestHttpServletResponse>();
            var chain = new Mock<ITestFilterChain>();

            request.Setup(x => x.GetAttribute("CsrfToken")).Returns((ITestCsrfToken)null);

            var filterObj = configurer.CsrfHeaderFilter();
            var filter = (CsrfHeaderFilterFake)filterObj;
            filter.DoFilter(request.Object, response.Object, chain.Object);

            response.Verify(x => x.AddCookie(It.IsAny<ITestCookie>()), Times.Never);
            chain.Verify(x => x.DoFilter(request.Object, response.Object), Times.Once);
        }

        [Fact]
        public void TestCsrfTokenRepository()
        {
            var configurer = new SsoApplication.LoginConfigurer();
            var repository = configurer.CsrfTokenRepository();
            Assert.NotNull(repository);

            var headerNameField = repository.GetType().GetField("headerName");
            Assert.NotNull(headerNameField);
            var value = headerNameField.GetValue(repository);
            Assert.Equal("X-XSRF-TOKEN", value);
        }
    }

    // Interfaces to simulate Java servlet test environment and enable mocking
    public interface ITestHttpServletRequest
    {
        object GetAttribute(string name);
    }
    public interface ITestHttpServletResponse
    {
        void AddCookie(ITestCookie cookie);
    }
    public interface ITestFilterChain
    {
        void DoFilter(object request, object response);
    }
    public interface ITestCsrfToken
    {
        string Token { get; }
    }
    public interface ITestCookie
    {
        string Name { get; }
        string Value { get; }
    }

    // Dummy implementation, not used directly in test, provided for completeness
    public class CsrfHeaderFilterFake
    {
        public void DoFilter(object request, object response, object chain)
        {
            var req = request as ITestHttpServletRequest;
            var resp = response as ITestHttpServletResponse;
            var fc = chain as ITestFilterChain;

            var csrfToken = req.GetAttribute("CsrfToken") as ITestCsrfToken;
            if (csrfToken != null)
            {
                var cookie = new TestCookie("XSRF-TOKEN", csrfToken.Token);
                resp.AddCookie(cookie);
            }
            fc.DoFilter(request, response);
        }
    }

    public class TestCookie : ITestCookie
    {
        public string Name { get; }
        public string Value { get; }
        public TestCookie(string name, string value)
        {
            Name = name;
            Value = value;
        }
    }
}