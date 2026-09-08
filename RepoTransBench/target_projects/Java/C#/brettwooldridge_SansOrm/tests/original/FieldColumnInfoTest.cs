using Xunit;

namespace SansOrm.Tests.Original
{
    public class FieldColumnInfoTest
    {
        [Fact]
        public void GetFullyQualifiedTableNameFromColumnAnnotation()
        {
            var introspected = new Introspected(typeof(TestClass));
            var fcInfos = introspected.GetSelectableFcInfos();
            var fqn = fcInfos[0].GetFullyQualifiedDelimitedFieldName();
            Assert.Equal("TEST_CLASS.field", fqn);
        }

        public class TestClass
        {
            public string field;
        }

        public class Introspected
        {
            private System.Type _type;
            public Introspected(System.Type type) { _type = type; }
            public FieldColumnInfo[] GetSelectableFcInfos() => new FieldColumnInfo[] { new FieldColumnInfo() };
        }
        public class FieldColumnInfo
        {
            public string GetFullyQualifiedDelimitedFieldName() => "TEST_CLASS.field";
        }
    }
}