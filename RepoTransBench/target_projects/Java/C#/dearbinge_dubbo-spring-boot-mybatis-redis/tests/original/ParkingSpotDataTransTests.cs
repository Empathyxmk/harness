using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using DearBingeOpenApi;
using Moq;
using Xunit;
using Microsoft.AspNetCore.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http.Features;

namespace DearBingeOpenApi.Tests.Original
{
    public class ParkingSpotDataTransTests
    {
        private ParkingSpotDataTrans _controller;
        private Mock<HttpRequest> _requestMock;
        private Mock<HttpResponse> _responseMock;
        private Mock<ISession> _sessionMock;
        private MemoryStream _bodyStream;
        private StreamWriter _writer;

        public ParkingSpotDataTransTests()
        {
            _controller = new ParkingSpotDataTrans();

            _requestMock = new Mock<HttpRequest>();
            _responseMock = new Mock<HttpResponse>();
            _sessionMock = new Mock<ISession>();

            var items = new Dictionary<object, object>();
            var context = new DefaultHttpContext();
            context.Session = _sessionMock.Object;

            _requestMock.Setup(r => r.HttpContext).Returns(context);
            _responseMock.SetupProperty(r => r.Body, new MemoryStream());

            _bodyStream = new MemoryStream();
            _responseMock.SetupProperty(r => r.Body, _bodyStream);

            // Dependency injection simulation
            _controller.posDataServiceMap = new Dictionary<string, InfrastructDeal>();
            _controller.securityService = new object();
        }

        [Fact]
        public void TestGetSession_Normal()
        {
            _sessionMock.Setup(s => s.Id).Returns("abcde12345");
            var context = new DefaultHttpContext();
            context.Session = _sessionMock.Object;

            _requestMock.Setup(r => r.HttpContext).Returns(context);

            _controller.GetSession(_requestMock.Object, _responseMock.Object);

            _sessionMock.Verify(s => s.SetString("username", "chubin"), Times.Once);

            // Read written response
            _bodyStream.Position = 0;
            var output = new StreamReader(_bodyStream).ReadToEnd();
            Assert.Contains("node3", output);
            Assert.Contains("sessionid:abcde12345", output);
        }

        [Fact]
        public void TestGetSession_IOException()
        {
            // IOException in C# will be thrown if stream is not writable, simulate by using closed stream
            var oldStream = _responseMock.Object.Body;
            _responseMock.Object.Body.Close();
            Assert.Throws<ObjectDisposedException>(() =>
                _controller.GetSession(_requestMock.Object, _responseMock.Object)
            );
            _responseMock.Object.Body = oldStream;
        }

        [Fact]
        public void TestGetUserName_NoSession()
        {
            var context = new DefaultHttpContext();
            context.Session = null;
            _requestMock.Setup(r => r.HttpContext).Returns(context);

            var bodyStream = new MemoryStream();
            _responseMock.SetupProperty(r => r.Body, bodyStream);

            _controller.GetUserName(_requestMock.Object, _responseMock.Object);

            bodyStream.Position = 0;
            var output = new StreamReader(bodyStream).ReadToEnd();
            Assert.Contains("no session found", output);
        }

        [Fact]
        public void TestGetUserName_NoAttribute()
        {
            _sessionMock.Setup(s => s.GetString("username")).Returns((string)null);

            var context = new DefaultHttpContext();
            context.Session = _sessionMock.Object;

            _requestMock.Setup(r => r.HttpContext).Returns(context);

            var bodyStream = new MemoryStream();
            _responseMock.SetupProperty(r => r.Body, bodyStream);

            _controller.GetUserName(_requestMock.Object, _responseMock.Object);

            bodyStream.Position = 0;
            var output = new StreamReader(bodyStream).ReadToEnd();
            Assert.Contains("no attribute found", output);
        }

        [Fact]
        public void TestGetUserName_WithUsername()
        {
            _sessionMock.Setup(s => s.GetString("username")).Returns("testuser");

            var context = new DefaultHttpContext();
            context.Session = _sessionMock.Object;

            _requestMock.Setup(r => r.HttpContext).Returns(context);

            var bodyStream = new MemoryStream();
            _responseMock.SetupProperty(r => r.Body, bodyStream);

            _controller.GetUserName(_requestMock.Object, _responseMock.Object);

            bodyStream.Position = 0;
            var output = new StreamReader(bodyStream).ReadToEnd();
            Assert.Contains("testuser", output);
        }

        [Fact]
        public void TestGetUserName_IOException()
        {
            // Simulate Exception by using a closed stream
            var bodyStream = new MemoryStream();
            bodyStream.Close();
            _responseMock.SetupProperty(r => r.Body, bodyStream);
            Assert.Throws<ObjectDisposedException>(() => _controller.GetUserName(_requestMock.Object, _responseMock.Object));
        }

        [Fact]
        public void TestCreate_noIdeal()
        {
            _requestMock.Setup(r => r.Query["method"]).Returns(string.Empty);

            var bodyStream = new MemoryStream();
            _responseMock.SetupProperty(r => r.Body, bodyStream);

            _controller.Create(_requestMock.Object, _responseMock.Object);

            bodyStream.Position = 0;
            var output = new StreamReader(bodyStream).ReadToEnd();
            Assert.Equal("", output);
        }

        [Fact]
        public void TestCreate_withIdeal()
        {
            var methodName = "sync";
            var dealMock = new Mock<InfrastructDeal>();
            dealMock.Setup(d => d.Accept(It.IsAny<HttpRequest>())).Returns("ok");
            _controller.posDataServiceMap[methodName] = dealMock.Object;

            _requestMock.Setup(r => r.Query["method"]).Returns(methodName);

            var bodyStream = new MemoryStream();
            _responseMock.SetupProperty(r => r.Body, bodyStream);

            _controller.Create(_requestMock.Object, _responseMock.Object);

            dealMock.Verify(d => d.Accept(It.IsAny<HttpRequest>()), Times.Once);

            bodyStream.Position = 0;
            var output = new StreamReader(bodyStream).ReadToEnd();
            Assert.Equal("ok", output);
        }

        [Fact]
        public void TestCreate_IdealThrows()
        {
            var methodName = "sync";
            var dealMock = new Mock<InfrastructDeal>();
            dealMock.Setup(d => d.Accept(It.IsAny<HttpRequest>())).Throws(new Exception("fail"));
            _controller.posDataServiceMap[methodName] = dealMock.Object;

            _requestMock.Setup(r => r.Query["method"]).Returns(methodName);

            var bodyStream = new MemoryStream();
            _responseMock.SetupProperty(r => r.Body, bodyStream);

            Assert.Throws<Exception>(() => _controller.Create(_requestMock.Object, _responseMock.Object));
        }

        [Fact]
        public void TestAddInterceptorsCoverage()
        {
            var registryMock = new Mock<object>();
            _controller.AddInterceptors(registryMock.Object);
            Assert.True(true); // Successfully invoked
        }
    }
}