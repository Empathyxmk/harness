using System;
using Xunit;
using FastDFSClient;

namespace FastDFSClient.PublicTests
{
    public class StructBasePublicTest
    {
        private class DummyStruct : StructBase
        {
            public string strVal;
            public long longVal;
            public int intVal;
            public int int32Val;
            public byte byteVal;
            public bool boolVal;
            public DateTime dateVal;

            public override void SetFields(byte[] bs, int offset)
            {
                var field = new FieldInfo("test", 0, 4);
                this.strVal = StringValue(bs, offset, field);
                this.longVal = LongValue(bs, offset, field);
                this.intVal = IntValue(bs, offset, field);
                this.int32Val = Int32Value(bs, offset, field);
                this.byteVal = ByteValue(bs, offset, field);
                this.boolVal = BooleanValue(bs, offset, field);
                this.dateVal = DateValue(bs, offset, field);
            }
        }

        static StructBasePublicTest()
        {
            try
            {
                ClientGlobal.g_charset = "UTF-8";
            }
            catch { }
        }

        [Fact]
        public void TestStringValueDifferent()
        {
            var s = new DummyStruct();
            var bs = System.Text.Encoding.UTF8.GetBytes("Public01\0\0");
            var f = new FieldInfo("str", 0, 8);
            string val = s.StringValue(bs, 0, f);
            Assert.Equal("Public01", val);
        }

        [Fact]
        public void TestStringValueEncodingExceptionPublic()
        {
            var s = new DummyStruct();
            var f = new FieldInfo("str", 0, 1);
            string origCharset = ClientGlobal.g_charset;
            ClientGlobal.g_charset = "unknown-charset";
            string val = s.StringValue(new byte[] { 66 }, 0, f);
            Assert.Null(val);
            ClientGlobal.g_charset = origCharset;
        }

        [Fact]
        public void TestOtherValueMethodsPublic()
        {
            var s = new DummyStruct();
            var bs = new byte[16];
            bs[0] = 42;
            var f = new FieldInfo("d", 0, 8);

            s.SetFields(bs, 0);
            Assert.NotNull(s.strVal);
            Assert.NotEqual(default(DateTime), s.dateVal);
            Assert.True(s.byteVal == bs[0]);
        }
    }
}