using System;
using Xunit;
using Moq;

namespace AndroidUtils.Tests
{
    public class AssetDatabaseOpenHelperTest
    {
        [Fact]
        public void TestGetDatabaseName()
        {
            var contextMock = new Mock<IContext>();
            var helper = new AssetDatabaseOpenHelper(contextMock.Object, "mydb.db");
            Assert.Equal("mydb.db", helper.GetDatabaseName());
        }

        [Fact]
        public void TestGetWritableDatabase_IOException()
        {
            var contextMock = new Mock<IContext>();
            var dbFileMock = new Mock<IFile>();
            contextMock.Setup(c => c.GetDatabasePath(It.IsAny<string>())).Returns(dbFileMock.Object);
            dbFileMock.Setup(f => f.Exists).Returns(false);

            var assetManagerMock = new Mock<IAssetManager>();
            contextMock.Setup(c => c.Assets).Returns(assetManagerMock.Object);
            assetManagerMock.Setup(am => am.Open("fail.db")).Throws(new System.IO.IOException("fail"));

            var helper = new AssetDatabaseOpenHelper(contextMock.Object, "fail.db");

            Assert.Throws<Exception>(() => helper.GetWritableDatabase());
        }
    }

    // Stubs and interfaces to simulate Android classes
    public interface IContext
    {
        IFile GetDatabasePath(string name);
        IAssetManager Assets { get; }
    }
    public interface IFile
    {
        bool Exists { get; }
    }
    public interface IAssetManager
    {
        System.IO.Stream Open(string name);
    }
    public class AssetDatabaseOpenHelper
    {
        private readonly IContext _context;
        private readonly string _dbName;

        public AssetDatabaseOpenHelper(IContext ctx, string dbName)
        {
            _context = ctx;
            _dbName = dbName;
        }

        public string GetDatabaseName()
        {
            return _dbName;
        }

        public object GetWritableDatabase()
        {
            var dbFile = _context.GetDatabasePath(_dbName);
            if (!dbFile.Exists)
            {
                try
                {
                    _context.Assets.Open(_dbName);
                }
                catch (System.IO.IOException)
                {
                    throw new Exception("fail");
                }
            }
            // Would return db connection
            return new object();
        }
    }
}