using Xunit;

namespace SansOrm.Tests.Public
{
    public class SansOrmPublicTest
    {
        private DataSourceStubPublic dataSource;
        private TransactionManagerStubPublic transactionManager;
        private UserTransactionStubPublic userTransaction;

        public SansOrmPublicTest()
        {
            dataSource = new DataSourceStubPublic();
            transactionManager = new TransactionManagerStubPublic();
            userTransaction = new UserTransactionStubPublic();
            SansOrm.Deinitialize();
        }

        [Fact]
        public void TestInitializeTxNone_Public()
        {
            var result = SansOrm.InitializeTxNone(dataSource);
            Assert.NotNull(result);
            Assert.Equal(dataSource, result);
        }

        [Fact]
        public void TestInitializeTxSimple_Public()
        {
            var result = SansOrm.InitializeTxSimple(dataSource);
            Assert.NotNull(result);
        }

        [Fact]
        public void TestInitializeTxCustom_Public()
        {
            var result = SansOrm.InitializeTxCustom(dataSource, transactionManager, userTransaction);
            Assert.Equal(dataSource, result);
        }

        [Fact]
        public void TestDeinitialize_Public()
        {
            SansOrm.InitializeTxCustom(dataSource, transactionManager, userTransaction);
            SansOrm.Deinitialize();
        }

        public class DataSourceStubPublic { }
        public class TransactionManagerStubPublic { }
        public class UserTransactionStubPublic { }

        public static class SansOrm
        {
            private static object _ds, _tm, _utx;
            public static object InitializeTxNone(object ds) { _ds = ds; return ds; }
            public static object InitializeTxSimple(object ds) { _ds = ds; return ds; }
            public static object InitializeTxCustom(object ds, object tm, object utx) { _ds = ds; _tm = tm; _utx = utx; return ds; }
            public static void Deinitialize() { _ds = null; _tm = null; _utx = null; }
        }
    }
}