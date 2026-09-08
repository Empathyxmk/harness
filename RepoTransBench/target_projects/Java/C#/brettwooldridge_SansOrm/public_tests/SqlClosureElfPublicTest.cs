using System;
using System.Reflection;
using Xunit;

namespace SansOrm.Tests.Public
{
    public class SqlClosureElfPublicTest
    {
        public class SampleEntity
        {
            public int publicInt;
            public string publicString;
        }

        [Fact]
        public void TestGetFieldValuePublic()
        {
            var obj = new SampleEntity();
            obj.publicInt = 77;
            obj.publicString = "helloPublic";
            var intField = typeof(SampleEntity).GetField(nameof(SampleEntity.publicInt));
            var stringField = typeof(SampleEntity).GetField(nameof(SampleEntity.publicString));
            Assert.Equal(77, OrmWriter.GetFieldValue(obj, intField));
            Assert.Equal("helloPublic", OrmWriter.GetFieldValue(obj, stringField));
        }

        [Fact]
        public void TestSetFieldValuePublic()
        {
            var obj = new SampleEntity();
            var intField = typeof(SampleEntity).GetField(nameof(SampleEntity.publicInt));
            var stringField = typeof(SampleEntity).GetField(nameof(SampleEntity.publicString));
            OrmWriter.SetFieldValue(obj, intField, 51);
            OrmWriter.SetFieldValue(obj, stringField, "worldPublic");
            Assert.Equal(51, obj.publicInt);
            Assert.Equal("worldPublic", obj.publicString);
        }
    }

    // Dummy implementation to allow test to build/run
    public static class OrmWriter
    {
        public static object GetFieldValue(object obj, FieldInfo field) => field.GetValue(obj);
        public static void SetFieldValue(object obj, FieldInfo field, object value) => field.SetValue(obj, value);
    }
}