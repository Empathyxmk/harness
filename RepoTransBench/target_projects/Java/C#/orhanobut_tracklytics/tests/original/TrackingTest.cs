using System;
using Xunit;
using System.Collections.Generic;
using Orhanobut.Tracklytics;

namespace Orhanobut.Sample.Tests
{
    public class TrackingTest
    {
        private readonly Dictionary<string, Event> triggeredEvents = new();

        public TrackingTest()
        {
            Tracklytics.Init(new TestEventSubscriber(e => triggeredEvents.Add(e.Name, e)));
        }

        [Fact]
        public void ConfirmKotlinAspects()
        {
            new FooKotlin().TrackFoo();
            Assert.Contains("event_kotlin", triggeredEvents.Keys);
        }

        [Fact]
        public void ConfirmJavaAspects()
        {
            new Foo().TrackFoo();
            Assert.Contains("event_java", triggeredEvents.Keys);
        }

        public class TestEventSubscriber : IEventSubscriber
        {
            private readonly Action<Event> _action;
            public TestEventSubscriber(Action<Event> onEvent) => _action = onEvent;
            public void OnEventTracked(Event e) => _action(e);
        }
    }
}