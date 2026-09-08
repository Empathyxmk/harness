using Xunit;
using Contacts;

namespace Contacts.OriginalTests
{
    public class EventTest
    {
        [Fact]
        public void TestConstructorsAndGetters_Type()
        {
            var e = new Event("2023-01-01", Event.Type.BIRTHDAY);
            Assert.Equal("2023-01-01", e.StartDate);
            Assert.Equal(Event.Type.BIRTHDAY, e.TypeValue);
            Assert.Null(e.Label);
        }

        [Fact]
        public void TestConstructorsAndGetters_Label()
        {
            var e = new Event("2023-01-01", "Anniversary");
            Assert.Equal("2023-01-01", e.StartDate);
            Assert.Equal(Event.Type.CUSTOM, e.TypeValue);
            Assert.Equal("Anniversary", e.Label);
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var e1 = new Event("2020-10-10", Event.Type.BIRTHDAY);
            var e2 = new Event("2020-10-10", Event.Type.BIRTHDAY);
            var e3 = new Event("2020-10-10", "CustomEvt");
            Assert.Equal(e1, e2);
            Assert.NotEqual(e1, e3);
            Assert.Equal(e1.GetHashCode(), e2.GetHashCode());
        }

        [Fact]
        public void TestTypeFromValue()
        {
            Assert.Equal(Event.Type.CUSTOM, Event.fromValue(0));
            Assert.Equal(Event.Type.ANNIVERSARY, Event.fromValue(1));
            Assert.Equal(Event.Type.OTHER, Event.fromValue(2));
            Assert.Equal(Event.Type.BIRTHDAY, Event.fromValue(3));
            Assert.Equal(Event.Type.UNKNOWN, Event.fromValue(99));
        }

        [Fact]
        public void TestNotEqualConditions()
        {
            var e1 = new Event("d", Event.Type.BIRTHDAY);
            Assert.False(e1.Equals(null));
            Assert.False(e1.Equals("notAnEvent"));
            var e2 = new Event("other", Event.Type.BIRTHDAY);
            Assert.NotEqual(e1, e2);
        }
    }
}