using System;
using System.Reflection;
using Xunit;
using Ainilife.ZebraDao;

namespace Ainilife.ZebraDao.Tests.Public
{
    public class AsyncDaoRunnableExecutorPublicTests
    {
        class DummyMapper
        {
            public string DoOtherStuff(string input) => new string(input.Reverse().ToArray());
            public void ThrowOtherError() => throw new Exception("boom2!");
        }

        [Fact]
        public void TestRunSuccess()
        {
            var mapper = new DummyMapper();
            var m = typeof(DummyMapper).GetMethod("DoOtherStuff");
            object successResult = null;
            Exception exceptionResult = null;

            var cb = new Callback<string>(
                v => successResult = v,
                e => exceptionResult = e
            );

            var exec = new AsyncDaoRunnableExecutor<string>(mapper, m, new object[] { "world" }, cb);
            exec.Run();

            Assert.Null(exceptionResult);
            Assert.Equal("dlrow", successResult);
        }

        [Fact]
        public void TestRunException()
        {
            var mapper = new DummyMapper();
            var m = typeof(DummyMapper).GetMethod("ThrowOtherError");
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
            Assert.Equal("boom2!", exceptionResult.InnerException?.Message);
        }

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