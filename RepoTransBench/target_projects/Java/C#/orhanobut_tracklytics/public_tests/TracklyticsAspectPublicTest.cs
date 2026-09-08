using System;
using System.Collections.Generic;
using System.Reflection;
using Xunit;
using Moq;
using FluentAssertions;

namespace Orhanobut.Tracklytics.PublicTests
{
    public class TracklyticsAspectPublicTest
    {
        private Mock<IProceedingJoinPoint> joinPointMock;
        private Mock<IMethodSignature> methodSignatureMock;

        private Dictionary<string, object> superAttributes;
        private TracklyticsAspect aspect;
        private TrackEvent trackEvent;
        private Dictionary<string, object> attributes;
        private IAspectListener aspectListener;

        public TracklyticsAspectPublicTest()
        {
            joinPointMock = new Mock<IProceedingJoinPoint>();
            methodSignatureMock = new Mock<IMethodSignature>();

            superAttributes = new Dictionary<string, object>();

            aspectListener = new TestAspectListener(
                (te, attrs) =>
                {
                    this.trackEvent = te;
                    this.attributes = attrs;
                },
                (k, v) => superAttributes[k] = v,
                k => superAttributes.Remove(k)
            );

            aspect = new TracklyticsAspect();
            aspect.Subscribe(aspectListener);

            joinPointMock.Setup(jp => jp.GetSignature()).Returns(methodSignatureMock.Object);
        }

        private MethodInfo InvokeMethod(Type klass, string methodName, params Type[] paramTypes)
        {
            var method = InitMethod(klass, methodName, paramTypes);
            var instance = Activator.CreateInstance(klass);
            joinPointMock.Setup(jp => jp.GetThis()).Returns(instance);
            aspect.WeaveJoinPointTrackEvent(joinPointMock.Object);
            return method;
        }

        private MethodInfo InitMethod(Type klass, string name, params Type[] parameterTypes)
        {
            var method = klass.GetMethod(name, parameterTypes);
            methodSignatureMock.Setup(m => m.GetMethod()).Returns(method);
            return method;
        }

        [Fact]
        public void TrackEventWithoutAttributesPublic()
        {
            var type = typeof(FakeBarClassNoAttributes);
            InvokeMethod(type, "Bar");
            AssertTrack()
                .Event("public_title")
                .NoFilters()
                .NoTags()
                .NoAttributes();
        }

        [Fact]
        public void UseReturnValueAsAttributePublic()
        {
            var type = typeof(FakeBarClassReturnAsAttribute);
            joinPointMock.Setup(jp => jp.Proceed()).Returns("bar_data");
            InvokeMethod(type, "Bar");
            AssertTrack()
                .Event("public_event")
                .NoTags()
                .NoFilters()
                .Attribute("pub_key", "bar_data");
        }

        [Fact]
        public void UseReturnValueAndParametersAsAttributesPublic()
        {
            var type = typeof(FakeBarClassReturnAndParamAsAttribute);
            joinPointMock.Setup(jp => jp.Proceed()).Returns("dataA");
            joinPointMock.Setup(jp => jp.GetArgs()).Returns(new object[] { "dataB" });
            InvokeMethod(type, "Bar", typeof(string));
            AssertTrack()
                .Event("eventA")
                .NoFilters()
                .NoTags()
                .Attribute("keyA", "dataA")
                .Attribute("keyB", "dataB");
        }

        [Fact]
        public void UseDefaultValueWhenThereIsNoReturnValuePublic()
        {
            var type = typeof(FakeBarClassDefaultValue);
            InvokeMethod(type, "Bar");
            AssertTrack()
                .Event("pubEv")
                .NoFilters()
                .NoTags()
                .Attribute("k1", "dfVal");
        }

        [Fact]
        public void UseDefaultValueWhenParameterValueIsNullPublic()
        {
            var type = typeof(FakeBarClassDefaultValueParam);
            joinPointMock.Setup(jp => jp.GetArgs()).Returns(new object[] { null });
            InvokeMethod(type, "Bar", typeof(string));
            AssertTrack()
                .Event("ev2")
                .NoFilters()
                .NoTags()
                .Attribute("kkk", "dvvv");
        }

        // Helper assertion class
        private TrackSession AssertTrack()
        {
            return new TrackSession(trackEvent, attributes);
        }

        private class TrackSession
        {
            private readonly TrackEvent _trackEvent;
            private readonly Dictionary<string, object> _attributes;
            public TrackSession(TrackEvent trackEvent, Dictionary<string, object> attributes)
            {
                _trackEvent = trackEvent;
                _attributes = attributes;
            }
            public TrackSession Event(string ev) { _trackEvent.Value().Should().Be(ev); return this; }
            public TrackSession NoFilters() { _trackEvent.Filters().Should().BeEmpty(); return this; }
            public TrackSession NoTags() { _trackEvent.Tags().Should().BeEmpty(); return this; }
            public TrackSession NoAttributes() { (_attributes == null || _attributes.Count == 0).Should().BeTrue(); return this; }
            public TrackSession Attribute(string key, object value) { _attributes[key].Should().Be(value); return this; }
        }

        private class TestAspectListener : IAspectListener
        {
            private readonly Action<TrackEvent, Dictionary<string, object>> _onAspectEvent;
            private readonly Action<string, object> _onSuperAdded;
            private readonly Action<string> _onSuperRemoved;

            public TestAspectListener(
                Action<TrackEvent, Dictionary<string, object>> onAspectEvent,
                Action<string, object> onSuperAdded,
                Action<string> onSuperRemoved)
            {
                _onAspectEvent = onAspectEvent; _onSuperAdded = onSuperAdded; _onSuperRemoved = onSuperRemoved;
            }
            public void OnAspectEventTriggered(TrackEvent trackEvent, Dictionary<string, object> attributes)
                => _onAspectEvent?.Invoke(trackEvent, attributes);
            public void OnAspectSuperAttributeAdded(string key, object value)
                => _onSuperAdded?.Invoke(key, value);
            public void OnAspectSuperAttributeRemoved(string key)
                => _onSuperRemoved?.Invoke(key);
        }

        public class FakeBarClassNoAttributes
        {
            [TrackEvent("public_title")]
            public void Bar() { }
        }

        public class FakeBarClassReturnAsAttribute
        {
            [TrackEvent("public_event")]
            [Attribute("pub_key")]
            public string Bar() => "bar_data";
        }

        public class FakeBarClassReturnAndParamAsAttribute
        {
            [TrackEvent("eventA")]
            [Attribute("keyA")]
            public string Bar([Attribute("keyB")] string param) => "dataA";
        }

        public class FakeBarClassDefaultValue
        {
            [TrackEvent("pubEv")]
            [Attribute(Value = "k1", DefaultValue = "dfVal")]
            public void Bar() { }
        }

        public class FakeBarClassDefaultValueParam
        {
            [TrackEvent("ev2")]
            public void Bar([Attribute(Value = "kkk", DefaultValue = "dvvv")] string val) { }
        }
    }
}