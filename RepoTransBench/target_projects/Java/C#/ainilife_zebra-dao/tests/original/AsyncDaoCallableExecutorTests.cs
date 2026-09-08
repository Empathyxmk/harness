using System;
using System.Reflection;
using Xunit;
using Ainilife.ZebraDao;

namespace Ainilife.ZebraDao.Tests.Original
{
    public class AsyncDaoCallableExecutorTests
    {
        class DummyMapper
        {
            public int Add(int a, int b) => a + b;
            public void ThrowError() => throw new Exception("fail");
        }

        [Fact]
        public void TestCallNormal()
        {
            var map = new DummyMapper();
            var m = typeof(DummyMapper).GetMethod("Add");
            var exec = new AsyncDaoCallableExecutor(map, m, new object[] { 3, 4 });
            var result = exec.Call();
            Assert.Equal(7, (int)result);
        }

        [Fact]
        public void TestCallThrowsException()
        {
            var map = new DummyMapper();
            var m = typeof(DummyMapper).GetMethod("ThrowError");
            var exec = new AsyncDaoCallableExecutor(map, m, null);

            var ex = Assert.Throws<TargetInvocationException>(() => exec.Call());
            Assert.Equal("fail", ex.InnerException?.Message);
        }
    }
}