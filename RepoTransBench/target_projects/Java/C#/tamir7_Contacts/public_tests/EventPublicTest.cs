using Xunit;
using Contacts;

namespace Contacts.PublicTests
{
    public class EventPublicTest
    {
        [Fact]
        public void TestConstructorsAndGetters_Type()
        {
            var e = new Event("2050-12-31", Event.Type.ANNIVERSARY);
            Assert.Equal("2050-12-31", e.StartDate);
            Assert.Equal(Event.Type.ANNIVERSARY, e.TypeValue);
            Assert.Null(e.Label);
        }

        [Fact]
        public void TestConstructorsAndGetters_Label()
        {
            var e = new Event("2024-07-14", "Special Date");
            Assert.Equal("2024-07-14", e.StartDate);
            Assert.Equal(Event.Type.CUSTOM, e.TypeValue);
            Assert.Equal("Special Date", e.Label);
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var e1 = new Event("2000-01-01", Event.Type.OTHER);
            var e2 = new Event("2000-01-01", Event.Type.OTHER);
            var e3 = new Event("2000-01-01", "Anniv");
            Assert.Equal(e1, e2);
            Assert.NotEqual(e1, e3);
            Assert.Equal(e1.GetHashCode(), e2.GetHashCode());
        }

        [Fact]
        public void TestTypeFromValue()
        {
            Assert.Equal(Event.Type.CUSTOM, Event.fromValue(-1));
            Assert.Equal(Event.Type.ANNIVERSARY, Event.fromValue(1));
            Assert.Equal(Event.Type.OTHER, Event.fromValue(2));
            Assert.Equal(Event.Type.BIRTHDAY, Event.fromValue(3));
            Assert.Equal(Event.Type.UNKNOWN, Event.fromValue(500));
        }

        [Fact]
        public void TestNotEqualConditions()
        {
            var e1 = new Event("2029-11-11", Event.Type.OTHER);
            Assert.False(e1.Equals(null));
            Assert.False(e1.Equals(new object()));
            var e2 = new Event("2222-02-22", Event.Type.OTHER);
            Assert.NotEqual(e1, e2);
        }
    }
}