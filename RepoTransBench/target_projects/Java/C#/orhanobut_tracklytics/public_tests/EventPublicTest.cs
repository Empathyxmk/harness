using System;
using System.Collections.Generic;
using Xunit;
using FluentAssertions;

namespace Orhanobut.Tracklytics.PublicTests
{
    public class EventPublicTest
    {
        class CustomTrackEvent : TrackEvent
        {
            public string Value() => "public_event";
            public int[] Filters() => new[] { 3, 4 };
            public string[] Tags() => new[] { "pub1", "pub2" };
        }

        [Fact]
        public void TestConstructorWithDifferentFields()
        {
            string name = "demo";
            int[] filters = new[] { 10, 20 };
            string[] tags = new[] { "alpha", "beta" };
            var attrs = new Dictionary<string, object> { ["m"] = "n" };
            var superAttrs = new Dictionary<string, object> { ["foo"] = "bar" };
            var ev = new Event(name, filters, tags, attrs, superAttrs);
            ev.Name.Should().Be(name);
            ev.Filters.Should().Equal(filters);
            ev.Tags.Should().Equal(tags);
            ev.Attributes.Should().BeEquivalentTo(attrs);
            ev.SuperAttributes.Should().BeEquivalentTo(superAttrs);
        }

        [Fact]
        public void TestConstructorWithDifferentTrackEvent()
        {
            TrackEvent te = new CustomTrackEvent();
            var attrs = new Dictionary<string, object> { ["x"] = 2 };
            var superAttrs = new Dictionary<string, object> { ["y"] = "z" };
            var ev = new Event(te, attrs, superAttrs);
            ev.Name.Should().Be("public_event");
            ev.Filters.Should().Equal(new[] { 3, 4 });
            ev.Tags.Should().Equal(new[] { "pub1", "pub2" });
            ev.Attributes.Should().BeEquivalentTo(attrs);
            ev.SuperAttributes.Should().BeEquivalentTo(superAttrs);
        }

        [Fact]
        public void TestGetAllAttributesDifferentKeys()
        {
            var attrs = new Dictionary<string, object> { ["jack"] = "jill" };
            var superAttrs = new Dictionary<string, object> { ["tango"] = "fox" };
            var ev = new Event("n2", Array.Empty<int>(), Array.Empty<string>(), attrs, superAttrs);
            var all = ev.GetAllAttributes();
            all.Count.Should().Be(2);
            all["jack"].Should().Be("jill");
            all["tango"].Should().Be("fox");
        }

        [Fact]
        public void TestGetAllAttributesSuperOverridesDifferent()
        {
            var attrs = new Dictionary<string, object> { ["theme"] = "dark", ["score"] = 100 };
            var superAttrs = new Dictionary<string, object> { ["theme"] = "light" };
            var ev = new Event("n3", Array.Empty<int>(), Array.Empty<string>(), attrs, superAttrs);
            var all = ev.GetAllAttributes();
            all.Count.Should().Be(2);
            all["theme"].Should().Be("light");
            all["score"].Should().Be(100);
        }

        [Fact]
        public void TestEmptyAttributesPublic()
        {
            var ev = new Event("public_event", Array.Empty<int>(), Array.Empty<string>(), new Dictionary<string, object>(), new Dictionary<string, object>());
            ev.GetAllAttributes().Should().NotBeNull();
            ev.GetAllAttributes().Should().BeEmpty();
        }
    }
}