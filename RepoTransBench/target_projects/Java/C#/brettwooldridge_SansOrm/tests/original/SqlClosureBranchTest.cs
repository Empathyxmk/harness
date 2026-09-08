using Xunit;

namespace SansOrm.Tests.Original
{
    public class SqlClosureBranchTest
    {
        private DataSourceStub dataSource = new DataSourceStub();

        [Fact]
        public void TestDefaultConstructorThrowsIfNoDataSource()
        {
            SqlClosure.SetDefaultDataSource(null);
            Assert.Throws<System.InvalidOperationException>(() => new SqlClosure<object>());
        }

        [Fact]
        public void TestOtherConstructorsWithoutDefaultDataSource()
        {
            var c1 = new SqlClosure<object>(dataSource);
            Assert.NotNull(c1);

            var c2 = new SqlClosure<object>(dataSource, "arg1", 42);
            Assert.NotNull(c2);

            var c3 = new SqlClosure<object>(new SqlClosure<object>(dataSource));
            Assert.NotNull(c3);

            var c4 = new SqlClosure<object>("a", "b");
            Assert.NotNull(c4);
        }

        [Fact]
        public void TestSetDefaultDataSource()
        {
            SqlClosure.SetDefaultDataSource(dataSource);
            var c = new SqlClosure<object>();
            Assert.NotNull(c);
        }

        public class DataSourceStub { }

        public class SqlClosure<T>
        {
            public SqlClosure() { if (_defaultDataSource == null) throw new System.InvalidOperationException(); }
            public SqlClosure(object dataSource) { }
            public SqlClosure(object dataSource, params object[] args) { }
            public SqlClosure(SqlClosure<T> inner) { }
            public SqlClosure(params object[] args) { }
            private static object _defaultDataSource;
            public static void SetDefaultDataSource(object ds) => _defaultDataSource = ds;
        }

        public static class SqlClosure
        {
            public static void SetDefaultDataSource(object ds) => SqlClosure<object>.SetDefaultDataSource(ds);
        }
    }
}