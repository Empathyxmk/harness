using System;
using System.Collections.Generic;
using Xunit;
using Moq;
using FluentAssertions;

namespace Orhanobut.Tracklytics.Tests
{
    public class TracklyticsTest
    {
        private Mock<IEventSubscriber> eventSubscriberMock;
        private Mock<ITrackEvent> trackEventMock;

        private Tracklytics tracklytics;

        public TracklyticsTest()
        {
            eventSubscriberMock = new Mock<IEventSubscriber>();
            trackEventMock = new Mock<ITrackEvent>();

            tracklytics = Tracklytics.Init(eventSubscriberMock.Object);

            eventSubscriberMock.Setup(x => x.ToString()).Returns("Tracklytics");
            trackEventMock.Setup(x => x.Value()).Returns("event");
            trackEventMock.Setup(x => x.Filters()).Returns(new[] { 1, 2 });
        }

        [Fact]
        public void TrackWithoutAnnotation()
        {
            var attributes = new Dictionary<string, object> { ["key"] = "value" };

            tracklytics.TrackEvent("event_name", attributes);

            eventSubscriberMock.Verify(sub => sub.OnEventTracked(It.Is<Event>(e =>
                e.Name == "event_name" &&
                e.Attributes["key"].Equals("value")
            )), Times.Once);
        }

        [Fact]
        public void TrackFromAspectEvent()
        {
            var trackEvent = new Mock<ITrackEvent>();
            trackEvent.Setup(x => x.Value()).Returns("event_name");
            var attributes = new Dictionary<string, object> { ["key"] = "value" };

            tracklytics.OnAspectEventTriggered(trackEvent.Object, attributes);

            eventSubscriberMock.Verify(sub => sub.OnEventTracked(It.Is<Event>(e =>
                e.Name == "event_name" &&
                e.Attributes["key"].Equals("value")
            )), Times.Once);
        }

        [Fact]
        public void TrackWithEvent()
        {
            tracklytics.TrackEvent("event_name");

            eventSubscriberMock.Verify(sub => sub.OnEventTracked(It.Is<Event>(e =>
                e.Name == "event_name" && e.Attributes == null
            )), Times.Once);
        }

        [Fact]
        public void AddSuperAttributesToEvent()
        {
            tracklytics.AddSuperAttribute("key1", "value1");
            tracklytics.AddSuperAttribute("key2", "value2");

            var attributes = new Dictionary<string, object> { ["key3"] = "value3" };

            tracklytics.TrackEvent("event_name", attributes);

            eventSubscriberMock.Verify(sub => sub.OnEventTracked(It.Is<Event>(e =>
                e.Name == "event_name" &&
                e.Attributes["key3"].Equals("value3") &&
                e.SuperAttributes["key1"].Equals("value1") &&
                e.SuperAttributes["key2"].Equals("value2")
            )), Times.Once);
        }

        [Fact]
        public void AddSuperAttributeFromAspects()
        {
            tracklytics.OnAspectSuperAttributeAdded("key1", "value1");

            tracklytics.TrackEvent("event_name");

            eventSubscriberMock.Verify(sub => sub.OnEventTracked(It.Is<Event>(e =>
                e.Name == "event_name" &&
                e.SuperAttributes["key1"].Equals("value1")
            )), Times.Once);
        }

        [Fact]
        public void RemoveSuperAttributes()
        {
            tracklytics.AddSuperAttribute("key1", "value1");
            tracklytics.AddSuperAttribute("key2", "value2");
            tracklytics.AddSuperAttribute("key3", "value3");

            tracklytics.RemoveSuperAttribute("key1");
            tracklytics.RemoveSuperAttribute("key2");

            var attributes = new Dictionary<string, object> { ["key4"] = "value4" };

            tracklytics.TrackEvent("event_name", attributes);

            eventSubscriberMock.Verify(sub => sub.OnEventTracked(It.Is<Event>(e =>
                e.Name == "event_name" &&
                e.Attributes["key4"].Equals("value4") &&
                e.SuperAttributes.Count == 1 &&
                e.SuperAttributes["key3"].Equals("value3")
            )), Times.Once);
        }

        [Fact]
        public void RemoveSuperAttributeFromAspects()
        {
            tracklytics.AddSuperAttribute("key1", "value1");
            tracklytics.AddSuperAttribute("key2", "value2");

            tracklytics.OnAspectSuperAttributeRemoved("key1");

            tracklytics.TrackEvent("event_name");

            eventSubscriberMock.Verify(sub => sub.OnEventTracked(It.Is<Event>(e =>
                e.Name == "event_name" &&
                e.SuperAttributes.Count == 1 &&
                e.SuperAttributes["key2"].Equals("value2")
            )), Times.Once);
        }

        [Fact]
        public void Log()
        {
            var loggerMock = new Mock<IEventLogListener>();
            tracklytics.SetEventLogListener(loggerMock.Object);

            var attributes = new Dictionary<string, object> { ["key"] = "value" };

            tracklytics.TrackEvent("event", attributes);

            loggerMock.Verify(x => x.Log("event-> {key=value}, super attrs: {}, filters: null"), Times.Once);
        }
    }
}