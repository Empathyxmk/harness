using System;
using System.Reflection;
using System.Threading;
using System.Threading.Tasks;
using Xunit;
using Ainilife.ZebraDao;

namespace Ainilife.ZebraDao.Tests.Public
{
    public class AsyncMapperExecutorPublicTests
    {
        class DummyMapper
        {
            public string Repeat(string input) => string.Concat(input, input);
            public string ThrowsOtherError() => throw new InvalidOperationException("fail!");
        }

        public AsyncMapperExecutorPublicTests()
        {
            AsyncMapperExecutor.Init(2, 3, 2);
        }

        [Fact]
        public async Task TestSubmitCallbackReturns()
        {
            var mapper = new DummyMapper();
            var m = typeof(DummyMapper).GetMethod("Repeat");
            var f = AsyncMapperExecutor.SubmitCallback(mapper, m, new object[] { "xyz" });
            var result = await f;
            Assert.Equal("xyzxyz", result);
        }

        [Fact]
        public async Task TestExecuteRunnableSuccess()
        {
            var mapper = new DummyMapper();
            var m = typeof(DummyMapper).GetMethod("Repeat");

            object result = null;
            Exception error = null;
            var cb = new Callback<string>(
                onSuccess: v => result = v,
                onException: e => error = e
            );

            AsyncMapperExecutor.ExecuteRunnable<string>(mapper, m, new object[] { "bar" }, cb);

            await Task.Delay(200);

            Assert.Equal("barbar", result);
            Assert.Null(error);
        }

        [Fact]
        public async Task TestExecuteRunnableThrows()
        {
            var mapper = new DummyMapper();
            var m = typeof(DummyMapper).GetMethod("ThrowsOtherError");

            object result = null;
            Exception error = null;
            var cb = new Callback<string>(
                onSuccess: v => result = v,
                onException: e => error = e
            );

            AsyncMapperExecutor.ExecuteRunnable<string>(mapper, m, null, cb);

            await Task.Delay(200);

            Assert.Null(result);
            Assert.NotNull(error);
            Assert.Equal("fail!", error.InnerException?.Message);
        }

        [Fact]
        public void TestCheckNullThrows()
        {
            var fi = typeof(AsyncMapperExecutor).GetField("_factory", BindingFlags.NonPublic | BindingFlags.Static);
            var prev = fi.GetValue(null);
            fi.SetValue(null, null);
            var ex = Assert.Throws<AsyncDaoException>(() =>
                AsyncMapperExecutor.SubmitCallback(new DummyMapper(),
                    typeof(DummyMapper).GetMethod("Repeat"),
                    new object[] { "xyz" }));
            Assert.Equal("AsyncMapperExecutor has not been init yet.", ex.Message);
            fi.SetValue(null, prev); // restore
        }

        [Fact]
        public void TestSetCorePoolSizeMethods()
        {
            AsyncMapperExecutor.SetCorePoolSize(2);
            AsyncMapperExecutor.SetMaximumPoolSize(3);
            Assert.True(true);
        }

        // Basic callback helper for easier lambda usage
        class Callback<T> : IAsyncDaoCallback<T>
        {
            private readonly Action<T> _onSuccess;
            private readonly Action<Exception> _onException;
            public Callback(Action<T> onSuccess, Action<Exception> onException)
            {
                _onSuccess = onSuccess;
                _onException = onException;
            }

            public void OnSuccess(T result) => _onSuccess(result);
            public void OnException(Exception ex) => _onException(ex);
        }
    }
}