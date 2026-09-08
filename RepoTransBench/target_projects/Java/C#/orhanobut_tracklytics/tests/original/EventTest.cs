using System;
using System.Collections.Generic;
using Xunit;
using FluentAssertions;

namespace Orhanobut.Tracklytics.Tests
{
    public class EventTest
    {
        class DummyTrackEvent : TrackEvent
        {
            public string Value() => "dummy_event";
            public int[] Filters() => new[] { 1, 2 };
            public string[] Tags() => new[] { "tag1", "tag2" };
        }

        [Fact]
        public void TestConstructorWithFields()
        {
            string name = "test";
            int[] filters = new[] { 1, 2 };
            string[] tags = new[] { "t1", "t2" };
            var attrs = new Dictionary<string, object> { ["a"] = "b" };
            var superAttrs = new Dictionary<string, object> { ["x"] = "y" };
            var ev = new Event(name, filters, tags, attrs, superAttrs);
            ev.Name.Should().Be(name);
            ev.Filters.Should().Equal(filters);
            ev.Tags.Should().Equal(tags);
            ev.Attributes.Should().BeEquivalentTo(attrs);
            ev.SuperAttributes.Should().BeEquivalentTo(superAttrs);
        }

        [Fact]
        public void TestConstructorWithTrackEvent()
        {
            TrackEvent te = new DummyTrackEvent();
            var attrs = new Dictionary<string, object> { ["c"] = 1 };
            var superAttrs = new Dictionary<string, object>();
            var ev = new Event(te, attrs, superAttrs);
            ev.Name.Should().Be("dummy_event");
            ev.Filters.Should().Equal(new[] { 1, 2 });
            ev.Tags.Should().Equal(new[] { "tag1", "tag2" });
            ev.Attributes.Should().BeEquivalentTo(attrs);
            ev.SuperAttributes.Should().BeEquivalentTo(superAttrs);
        }

        [Fact]
        public void TestGetAllAttributesNoOverlap()
        {
            var attrs = new Dictionary<string, object> { ["foo"] = "bar" };
            var superAttrs = new Dictionary<string, object> { ["hello"] = "world" };
            var ev = new Event("n", Array.Empty<int>(), Array.Empty<string>(), attrs, superAttrs);
            var all = ev.GetAllAttributes();
            all.Count.Should().Be(2);
            all["foo"].Should().Be("bar");
            all["hello"].Should().Be("world");
        }

        [Fact]
        public void TestGetAllAttributesSuperOverridesNormal()
        {
            var attrs = new Dictionary<string, object> { ["foo"] = "bar", ["a"] = 1 };
            var superAttrs = new Dictionary<string, object> { ["foo"] = "baz" };
            var ev = new Event("n", Array.Empty<int>(), Array.Empty<string>(), attrs, superAttrs);
            var all = ev.GetAllAttributes();
            all.Count.Should().Be(2);
            all["foo"].Should().Be("baz");
            all["a"].Should().Be(1);
        }

        [Fact]
        public void TestEmptyAttributes()
        {
            var ev = new Event("event", Array.Empty<int>(), Array.Empty<string>(), new Dictionary<string, object>(), new Dictionary<string, object>());
            ev.GetAllAttributes().Should().NotBeNull();
            ev.GetAllAttributes().Should().BeEmpty();
        }
    }
}