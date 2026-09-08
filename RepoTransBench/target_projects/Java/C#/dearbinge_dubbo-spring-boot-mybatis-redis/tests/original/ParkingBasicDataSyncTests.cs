using DearBingeOpenApi.Service.Impl;
using Xunit;
using Moq;
using Microsoft.AspNetCore.Http;

namespace DearBingeOpenApi.Tests.Original
{
    public class ParkingBasicDataSyncTests
    {
        private ParkingBasicDataSync _dataSync;

        public ParkingBasicDataSyncTests()
        {
            _dataSync = new ParkingBasicDataSync();
        }

        [Fact]
        public void TestAcceptReturnsSuccess()
        {
            var requestMock = new Mock<HttpRequest>();
            requestMock.Setup(r => r.Query["jsonBody"]).Returns("{\"key\":\"value\"}");

            var result = _dataSync.Accept(requestMock.Object);
            Assert.Contains("success", result);
        }

        [Fact]
        public void TestAcceptReturnsFail()
        {
            var requestMock = new Mock<HttpRequest>();
            requestMock.Setup(r => r.Query["jsonBody"]).Returns((string)null);

            var result = _dataSync.Accept(requestMock.Object);
            Assert.Contains("fail", result);
        }

        [Fact]
        public void TestAcceptExceptionInParameter()
        {
            var requestMock = new Mock<HttpRequest>();
            requestMock.Setup(r => r.Query["jsonBody"]).Throws(new System.Exception("error"));

            var result = _dataSync.Accept(requestMock.Object);
            Assert.Contains("fail", result);
        }
    }
}