using System;
using System.Reflection;
using Xunit;
using Ainilife.ZebraDao;

namespace Ainilife.ZebraDao.Tests.Original
{
    public class AsyncDaoRunnableExecutorTests
    {
        class DummyMapper
        {
            public string DoStuff(string input) => input.ToUpperInvariant();
            public void ThrowError() => throw new Exception("boom!");
        }

        [Fact]
        public void TestRunSuccess()
        {
            var mapper = new DummyMapper();
            var m = typeof(DummyMapper).GetMethod("DoStuff");
            object successResult = null;
            Exception exceptionResult = null;

            var cb = new Callback<string>(
                v => successResult = v,
                e => exceptionResult = e
            );

            var exec = new AsyncDaoRunnableExecutor<string>(mapper, m, new object[] { "hello" }, cb);
            exec.Run();

            Assert.Null(exceptionResult);
            Assert.Equal("HELLO", successResult);
        }

        [Fact]
        public void TestRunException()
        {
            var mapper = new DummyMapper();
            var m = typeof(DummyMapper).GetMethod("ThrowError");
            object successResult = null;
            Exception exceptionResult = null;

            var cb = new Callback<string>(
                v => successResult = v,
                e => exceptionResult = e
            );

            var exec = new AsyncDaoRunnableExecutor<string>(mapper, m, null, cb);
            exec.Run();

            Assert.Null(successResult);
            Assert.NotNull(exceptionResult);
            Assert.Equal("boom!", exceptionResult.InnerException?.Message);
        }

        // Helper
        class Callback<T> : IAsyncDaoCallback<T>
        {
            private readonly Action<T> _success;
            private readonly Action<Exception> _fail;
            public Callback(Action<T> success, Action<Exception> fail)
            {
                _success = success;
                _fail = fail;
            }
            public void OnSuccess(T result) => _success(result);
            public void OnException(Exception ex) => _fail(ex);
        }
    }
}