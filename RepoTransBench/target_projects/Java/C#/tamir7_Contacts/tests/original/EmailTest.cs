using Xunit;
using Contacts;

namespace Contacts.OriginalTests
{
    public class EmailTest
    {
        [Fact]
        public void TestConstructorsAndGetters_Type()
        {
            var e = new Email("addr@email.com", Email.Type.WORK);
            Assert.Equal("addr@email.com", e.Address);
            Assert.Equal(Email.Type.WORK, e.TypeValue);
            Assert.Null(e.Label);
        }

        [Fact]
        public void TestConstructorsAndGetters_Label()
        {
            var e = new Email("foo@bar.com", "mylabel");
            Assert.Equal("foo@bar.com", e.Address);
            Assert.Equal(Email.Type.CUSTOM, e.TypeValue);
            Assert.Equal("mylabel", e.Label);
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var e1 = new Email("x@x.com", Email.Type.HOME);
            var e2 = new Email("x@x.com", Email.Type.HOME);
            var e3 = new Email("x@x.com", "label");
            Assert.Equal(e1, e2);
            Assert.NotEqual(e1, e3);
            Assert.Equal(e1.GetHashCode(), e2.GetHashCode());
        }

        [Fact]
        public void TestTypeFromValue()
        {
            Assert.Equal(Email.Type.CUSTOM, Email.fromValue(0));
            Assert.Equal(Email.Type.HOME, Email.fromValue(1));
            Assert.Equal(Email.Type.WORK, Email.fromValue(2));
            Assert.Equal(Email.Type.OTHER, Email.fromValue(3));
            Assert.Equal(Email.Type.MOBILE, Email.fromValue(4));
            Assert.Equal(Email.Type.UNKNOWN, Email.fromValue(99));
        }

        [Fact]
        public void TestNotEqualConditions()
        {
            var e1 = new Email("x@x.com", Email.Type.HOME);
            Assert.False(e1.Equals(null));
            Assert.False(e1.Equals("notAnEmail"));
            var e2 = new Email("z@z.com", Email.Type.HOME);
            Assert.NotEqual(e1, e2);
        }
    }
}