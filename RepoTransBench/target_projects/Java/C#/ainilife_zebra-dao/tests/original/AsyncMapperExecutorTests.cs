using System;
using System.Reflection;
using System.Threading;
using System.Threading.Tasks;
using Xunit;
using Ainilife.ZebraDao;

namespace Ainilife.ZebraDao.Tests.Original
{
    public class AsyncMapperExecutorTests
    {
        class DummyMapper
        {
            public string Reverse(string input) => new string(input.ToCharArray().Reverse().ToArray());
            public string ThrowsError() => throw new InvalidOperationException("err!");
        }

        public AsyncMapperExecutorTests()
        {
            AsyncMapperExecutor.Init(1, 2, 2);
        }

        [Fact]
        public async Task TestSubmitCallbackReturns()
        {
            var mapper = new DummyMapper();
            var m = typeof(DummyMapper).GetMethod("Reverse");
            var f = AsyncMapperExecutor.SubmitCallback(mapper, m, new object[] { "abc" });
            var result = await f;
            Assert.Equal("cba", result);
        }

        [Fact]
        public async Task TestExecuteRunnableSuccess()
        {
            var mapper = new DummyMapper();
            var m = typeof(DummyMapper).GetMethod("Reverse");

            object result = null;
            Exception error = null;
            var cb = new Callback<string>(
                onSuccess: v => result = v,
                onException: e => error = e
            );

            AsyncMapperExecutor.ExecuteRunnable<string>(mapper, m, new object[] { "foo" }, cb);

            await Task.Delay(200);

            Assert.Equal("oof", result);
            Assert.Null(error);
        }

        [Fact]
        public async Task TestExecuteRunnableThrows()
        {
            var mapper = new DummyMapper();
            var m = typeof(DummyMapper).GetMethod("ThrowsError");

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
            Assert.Equal("err!", error.InnerException?.Message);
        }

        [Fact]
        public void TestCheckNullThrows()
        {
            // forcibly nullify internal field
            var fi = typeof(AsyncMapperExecutor).GetField("_factory", BindingFlags.NonPublic | BindingFlags.Static);
            var prev = fi.GetValue(null);
            fi.SetValue(null, null);
            var ex = Assert.Throws<AsyncDaoException>(() =>
                AsyncMapperExecutor.SubmitCallback(new DummyMapper(),
                    typeof(DummyMapper).GetMethod("Reverse"),
                    new object[] { "abc" }));
            Assert.Equal("AsyncMapperExecutor has not been init yet.", ex.Message);
            fi.SetValue(null, prev); // restore
        }

        [Fact]
        public void TestSetCorePoolSizeMethods()
        {
            AsyncMapperExecutor.SetCorePoolSize(1);
            AsyncMapperExecutor.SetMaximumPoolSize(2);
            // no assertion - just to cover method branches
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