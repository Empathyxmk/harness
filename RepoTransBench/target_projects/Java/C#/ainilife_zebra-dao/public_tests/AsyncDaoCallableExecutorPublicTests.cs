using System;
using System.Reflection;
using Xunit;
using Ainilife.ZebraDao;

namespace Ainilife.ZebraDao.Tests.Public
{
    public class AsyncDaoCallableExecutorPublicTests
    {
        class DummyCallable
        {
            public int Calc(int a, int b) => a - b;
            public int ThrowSomething() => throw new ArgumentException("sub_fail");
        }

        [Fact]
        public void TestCallableRunSuccess()
        {
            var inst = new DummyCallable();
            var method = typeof(DummyCallable).GetMethod("Calc");
            object output = null;
            Exception err = null;

            var cb = new Callback<int>(
                v => output = v,
                e => err = e
            );

            var exec = new Ainilife.ZebraDao.AsyncDaoCallableExecutor<int>(inst, method, new object[] { 8, 3 }, cb);
            var val = exec.Call();

            Assert.Equal(5, val);
            Assert.Null(err);
            Assert.Equal(5, output);
        }

        [Fact]
        public void TestCallableThrowsException()
        {
            var inst = new DummyCallable();
            var method = typeof(DummyCallable).GetMethod("ThrowSomething");
            object output = null;
            Exception err = null;
            bool exceptionFired = false;

            var cb = new Callback<int>(
                v => output = v,
                e => { err = e; exceptionFired = true; }
            );

            var exec = new Ainilife.ZebraDao.AsyncDaoCallableExecutor<int>(inst, method, null, cb);
            var ex = Assert.Throws<TargetInvocationException>(() => exec.Call());

            Assert.Null(output);
            Assert.True(exceptionFired);
            Assert.NotNull(err);
            Assert.Equal("sub_fail", err.InnerException?.Message);
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