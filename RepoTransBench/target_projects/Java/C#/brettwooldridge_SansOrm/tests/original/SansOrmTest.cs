using Xunit;

namespace SansOrm.Tests.Original
{
    public class SansOrmTest
    {
        private DataSourceStub dataSource = new DataSourceStub();
        private TransactionManagerStub transactionManager = new TransactionManagerStub();
        private UserTransactionStub userTransaction = new UserTransactionStub();

        public SansOrmTest()
        {
            SansOrm.Deinitialize();
        }

        [Fact]
        public void TestInitializeTxNone()
        {
            var result = SansOrm.InitializeTxNone(dataSource);
            Assert.NotNull(result);
            Assert.Equal(dataSource, result);
        }

        [Fact]
        public void TestInitializeTxSimple()
        {
            var result = SansOrm.InitializeTxSimple(dataSource);
            Assert.NotNull(result);
        }

        [Fact]
        public void TestInitializeTxCustom()
        {
            var result = SansOrm.InitializeTxCustom(dataSource, transactionManager, userTransaction);
            Assert.Equal(dataSource, result);
        }

        [Fact]
        public void TestDeinitialize()
        {
            SansOrm.InitializeTxCustom(dataSource, transactionManager, userTransaction);
            SansOrm.Deinitialize();
        }

        public class DataSourceStub { }
        public class TransactionManagerStub { }
        public class UserTransactionStub { }

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