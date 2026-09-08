using System;
using Moq;
using Xunit;

namespace GoogleMailImporter.PublicTests.Gmail
{
    public class UnsuccessfulResponseHandlerChainerPublicTests
    {
        [Fact]
        public void TestDifferentInterceptorChainDelegates()
        {
            var interceptor1 = new Mock<IHttpResponseInterceptor>();
            var interceptor2 = new Mock<IHttpResponseInterceptor>();
            var response = new object();
            var chain = new UnsuccessfulResponseHandlerChainer(interceptor1.Object, interceptor2.Object);

            chain.InterceptResponse(response);

            interceptor1.Verify(i => i.InterceptResponse(response));
            interceptor2.Verify(i => i.InterceptResponse(response));
        }
    }

    public interface IHttpResponseInterceptor
    {
        void InterceptResponse(object response);
    }

    public class UnsuccessfulResponseHandlerChainer
    {
        private readonly IHttpResponseInterceptor[] _interceptors;
        public UnsuccessfulResponseHandlerChainer(params IHttpResponseInterceptor[] interceptors)
        {
            _interceptors = interceptors;
        }
        public void InterceptResponse(object response)
        {
            foreach (var interceptor in _interceptors)
                interceptor.InterceptResponse(response);
        }
    }
}