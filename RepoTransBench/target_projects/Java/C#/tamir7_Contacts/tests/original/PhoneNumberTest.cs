using Xunit;
using Contacts;

namespace Contacts.OriginalTests
{
    public class PhoneNumberTest
    {
        [Fact]
        public void TestConstructorsAndGetters_Type()
        {
            var p = new PhoneNumber("12345", PhoneNumber.Type.HOME, "54321");
            Assert.Equal("12345", p.Number);
            Assert.Equal("54321", p.NormalizedNumber);
            Assert.Equal(PhoneNumber.Type.HOME, p.TypeValue);
            Assert.Null(p.Label);
        }

        [Fact]
        public void TestConstructorsAndGetters_Label()
        {
            var p = new PhoneNumber("333", "mobile label", "333");
            Assert.Equal("333", p.Number);
            Assert.Equal("mobile label", p.Label);
            Assert.Equal(PhoneNumber.Type.CUSTOM, p.TypeValue);
            Assert.Equal("333", p.NormalizedNumber);
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var p1 = new PhoneNumber("123", PhoneNumber.Type.HOME, "abc");
            var p2 = new PhoneNumber("123", PhoneNumber.Type.HOME, "abc");
            var p3 = new PhoneNumber("999", PhoneNumber.Type.HOME, "abc");
            Assert.Equal(p1, p2);
            Assert.NotEqual(p1, p3);
            Assert.Equal(p1.GetHashCode(), p2.GetHashCode());
        }

        [Fact]
        public void TestTypeFromValue()
        {
            Assert.Equal(PhoneNumber.Type.CUSTOM, PhoneNumber.fromValue(0));
            Assert.Equal(PhoneNumber.Type.HOME, PhoneNumber.fromValue(1));
            Assert.Equal(PhoneNumber.Type.MOBILE, PhoneNumber.fromValue(2));
            Assert.Equal(PhoneNumber.Type.WORK, PhoneNumber.fromValue(3));
            Assert.Equal(PhoneNumber.Type.FAX_WORK, PhoneNumber.fromValue(4));
            Assert.Equal(PhoneNumber.Type.FAX_HOME, PhoneNumber.fromValue(5));
            Assert.Equal(PhoneNumber.Type.PAGER, PhoneNumber.fromValue(6));
            Assert.Equal(PhoneNumber.Type.OTHER, PhoneNumber.fromValue(7));
            Assert.Equal(PhoneNumber.Type.CALLBACK, PhoneNumber.fromValue(8));
            Assert.Equal(PhoneNumber.Type.CAR, PhoneNumber.fromValue(9));
            Assert.Equal(PhoneNumber.Type.COMPANY_MAIN, PhoneNumber.fromValue(10));
            Assert.Equal(PhoneNumber.Type.ISDN, PhoneNumber.fromValue(11));
            Assert.Equal(PhoneNumber.Type.MAIN, PhoneNumber.fromValue(12));
            Assert.Equal(PhoneNumber.Type.OTHER_FAX, PhoneNumber.fromValue(13));
            Assert.Equal(PhoneNumber.Type.RADIO, PhoneNumber.fromValue(14));
            Assert.Equal(PhoneNumber.Type.TELEX, PhoneNumber.fromValue(15));
            Assert.Equal(PhoneNumber.Type.TTY_TDD, PhoneNumber.fromValue(16));
            Assert.Equal(PhoneNumber.Type.WORK_MOBILE, PhoneNumber.fromValue(17));
            Assert.Equal(PhoneNumber.Type.WORK_PAGER, PhoneNumber.fromValue(18));
            Assert.Equal(PhoneNumber.Type.ASSISTANT, PhoneNumber.fromValue(19));
            Assert.Equal(PhoneNumber.Type.MMS, PhoneNumber.fromValue(20));
            Assert.Equal(PhoneNumber.Type.UNKNOWN, PhoneNumber.fromValue(999));
        }

        [Fact]
        public void TestNotEqualConditions()
        {
            var p1 = new PhoneNumber("x", PhoneNumber.Type.HOME, "n");
            Assert.False(p1.Equals(null));
            Assert.False(p1.Equals("notPhone"));
            var p2 = new PhoneNumber("different", PhoneNumber.Type.HOME, "n");
            Assert.NotEqual(p1, p2);
        }
    }
}