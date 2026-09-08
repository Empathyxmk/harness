using System;
using Xunit;
using FastDFSClient;

namespace FastDFSClient.Tests
{
    public class StructBaseTest
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

        static StructBaseTest()
        {
            // Setup static charset for testing
            try
            {
                ClientGlobal.g_charset = "UTF-8";
            }
            catch { }
        }

        [Fact]
        public void TestStringValueNormal()
        {
            var s = new DummyStruct();
            var bs = System.Text.Encoding.UTF8.GetBytes("TestStr\0\0\0");
            var f = new FieldInfo("str", 0, 7);
            string val = s.StringValue(bs, 0, f);
            Assert.Equal("TestStr", val);
        }

        [Fact]
        public void TestStringValueEncodingException()
        {
            var s = new DummyStruct();
            var f = new FieldInfo("str", 0, 1);
            string origCharset = ClientGlobal.g_charset;
            ClientGlobal.g_charset = "invalid-charset";
            string val = s.StringValue(new byte[] { 65 }, 0, f);
            Assert.Null(val);
            ClientGlobal.g_charset = origCharset;
        }

        [Fact]
        public void TestOtherValueMethods()
        {
            var s = new DummyStruct();
            var bs = new byte[16];
            bs[0] = 100;
            var f = new FieldInfo("d", 0, 8);
            s.SetFields(bs, 0);
            Assert.NotNull(s.strVal);
            Assert.NotEqual(default(DateTime), s.dateVal);
            Assert.True(s.byteVal == bs[0]);
        }
    }
}