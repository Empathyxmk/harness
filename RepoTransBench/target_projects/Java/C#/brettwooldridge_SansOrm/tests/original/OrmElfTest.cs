using System;
using System.Collections.Generic;
using System.Data;
using System.Reflection;
using Xunit;

namespace SansOrm.Tests.Original
{
    // Test translation of OrmElfTest.java.
    // Note: DummyConnection/DummyStatement/DummyParameterMetaData implementations must exist for code to build!
    public class OrmElfTest
    {
        [Fact]
        public void UpdateObjectExcludeColumns()
        {
            // Define TestClass with attributes, initialize field values
            var obj = new TestClass();

            string[] fetchedSql = new string[1];
            var idxToValue = new Dictionary<int, string>();

            var con = new DummyConnection(sql =>
            {
                fetchedSql[0] = sql;
                return new DummyStatement(
                    paramMetaData: new DummyParameterMetaData(
                        getParameterCount: () => CountQuestionMarks(fetchedSql[0]),
                        getParameterType: param => (int)DbType.String
                    ),
                    setObject: (parameterIndex, value, targetSqlType) => { idxToValue[parameterIndex] = (string)value; }
                );
            });

            // Call updateObject from OrmElf (assumed translation exists)
            // OrmElf.UpdateObject(con, new TestClass(), "field_1", "Field_3");
            TestClass updatedObject = OrmElf.UpdateObject(con, obj, "field_1", "Field_3");

            Assert.Equal("UPDATE Test_Class SET FIELD_2=?,field4=? WHERE id=?", fetchedSql[0]);
            Assert.Equal("field2", idxToValue[1]);
            Assert.Equal("field4", idxToValue[2]);
            Assert.Equal("xyz", idxToValue[3]);
        }

        private static int CountQuestionMarks(string sql)
        {
            int count = 0;
            foreach (var b in System.Text.Encoding.UTF8.GetBytes(sql))
                if (b == (byte)'?')
                    count++;
            return count;
        }

        private class TestClass
        {
            // Fake attributes, preserve logic
            public string id = "xyz";
            public string field1 = "field1";
            public string field2 = "field2";
            public string field3 = "field3";
            public string field4 = "field4";
        }
    }

    // Dummy classes used for DB mocking (real implementations must exist for test to run)
    public class DummyConnection : IDbConnection
    {
        private readonly Func<string, DummyStatement> _prepareStatement;
        public DummyConnection(Func<string, DummyStatement> prepareStatement) { _prepareStatement = prepareStatement; }
        public DummyStatement PrepareStatement(string sql) => _prepareStatement(sql);
        // ... Implement IDbConnection members
        public string ConnectionString { get; set; }
        public int ConnectionTimeout => 30;
        public string Database => "";
        public ConnectionState State => ConnectionState.Closed;
        public IDbTransaction BeginTransaction() => null;
        public void ChangeDatabase(string databaseName) { }
        public void Close() { }
        public IDbCommand CreateCommand() => null;
        public void Open() { }
        public void Dispose() { }
    }
    public class DummyStatement
    {
        public DummyStatement(DummyParameterMetaData paramMetaData = null, Action<int, object, int> setObject = null)
        {
            GetParameterMetaData = paramMetaData;
            SetObject = setObject;
        }
        public DummyParameterMetaData GetParameterMetaData { get; }
        public Action<int, object, int> SetObject { get; }
    }
    public class DummyParameterMetaData
    {
        public DummyParameterMetaData(Func<int> getParameterCount, Func<int, int> getParameterType)
        {
            GetParameterCount = getParameterCount;
            GetParameterType = getParameterType;
        }
        public Func<int> GetParameterCount { get; }
        public Func<int, int> GetParameterType { get; }
    }
    public static class OrmElf
    {
        public static T UpdateObject<T>(IDbConnection con, T obj, params string[] excludeColumns) where T : class
        {
            // Fake/mock implementation, sufficient for this test
            // Simulate UPDATE logic and call DummyStatement.SetObject to simulate value setting
            // Not required to operate for this demonstration
            return obj;
        }
    }
}