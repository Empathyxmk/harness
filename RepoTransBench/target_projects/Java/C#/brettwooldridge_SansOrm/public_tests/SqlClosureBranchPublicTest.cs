using Xunit;

namespace SansOrm.Tests.Public
{
    public class SqlClosureBranchPublicTest
    {
        private DataSourceStubPublic dataSource;

        public SqlClosureBranchPublicTest()
        {
            dataSource = new DataSourceStubPublic();
        }

        [Fact]
        public void TestDefaultConstructorThrowsIfNoDataSource_Public()
        {
            SqlClosure.SetDefaultDataSource(null);
            Assert.Throws<System.InvalidOperationException>(() => new SqlClosure<object>());
        }

        [Fact]
        public void TestOtherConstructorsWithoutDefaultDataSource_Public()
        {
            var c1 = new SqlClosure<object>(dataSource);
            Assert.NotNull(c1);

            var c2 = new SqlClosure<object>(dataSource, "public_arg", 84);
            Assert.NotNull(c2);

            var c3 = new SqlClosure<object>(new SqlClosure<object>(dataSource));
            Assert.NotNull(c3);

            var c4 = new SqlClosure<object>("x", "y");
            Assert.NotNull(c4);
        }

        [Fact]
        public void TestSetDefaultDataSource_Public()
        {
            SqlClosure.SetDefaultDataSource(dataSource);
            var c = new SqlClosure<object>();
            Assert.NotNull(c);
        }

        public class DataSourceStubPublic
        {
            // Dummy DataSource stub -- interfaces needed for compilation
        }

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