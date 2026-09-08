using Xunit;
using Contacts;

namespace Contacts.PublicTests
{
    public class EmailPublicTest
    {
        [Fact]
        public void TestConstructorsAndGetters_Type()
        {
            var e = new Email("test@public.com", Email.Type.HOME);
            Assert.Equal("test@public.com", e.Address);
            Assert.Equal(Email.Type.HOME, e.TypeValue);
            Assert.Null(e.Label);
        }

        [Fact]
        public void TestConstructorsAndGetters_Label()
        {
            var e = new Email("alpha@beta.com", "office");
            Assert.Equal("alpha@beta.com", e.Address);
            Assert.Equal(Email.Type.CUSTOM, e.TypeValue);
            Assert.Equal("office", e.Label);
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var e1 = new Email("unique@mail.com", Email.Type.MOBILE);
            var e2 = new Email("unique@mail.com", Email.Type.MOBILE);
            var e3 = new Email("unique@mail.com", "project");
            Assert.Equal(e1, e2);
            Assert.NotEqual(e1, e3);
            Assert.Equal(e1.GetHashCode(), e2.GetHashCode());
        }

        [Fact]
        public void TestTypeFromValue()
        {
            Assert.Equal(Email.Type.CUSTOM, Email.fromValue(-1));
            Assert.Equal(Email.Type.HOME, Email.fromValue(1));
            Assert.Equal(Email.Type.WORK, Email.fromValue(2));
            Assert.Equal(Email.Type.OTHER, Email.fromValue(3));
            Assert.Equal(Email.Type.MOBILE, Email.fromValue(4));
            Assert.Equal(Email.Type.UNKNOWN, Email.fromValue(123));
        }

        [Fact]
        public void TestNotEqualConditions()
        {
            var e1 = new Email("nobody@nowhere.com", Email.Type.MOBILE);
            Assert.False(e1.Equals(null));
            Assert.False(e1.Equals("NotAnEmailObject"));
            var e2 = new Email("someone@somewhere.com", Email.Type.MOBILE);
            Assert.NotEqual(e1, e2);
        }
    }
}