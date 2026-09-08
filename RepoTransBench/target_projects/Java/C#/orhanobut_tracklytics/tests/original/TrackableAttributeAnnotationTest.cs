using System;
using System.Linq;
using System.Reflection;
using Xunit;

namespace Orhanobut.Tracklytics.Tests
{
    public class TrackableAttributeAnnotationTest
    {
        class Dummy
        {
            [TrackableAttribute]
            public void AnnotatedMethod([TrackableAttribute] string param) { }
        }

        [Fact]
        public void TestTrackableAttributeOnMethod()
        {
            MethodInfo m = typeof(Dummy).GetMethod("AnnotatedMethod");
            Assert.True(m.GetCustomAttributes(typeof(TrackableAttribute), false).Any());
        }

        [Fact]
        public void TestTrackableAttributeOnParameter()
        {
            MethodInfo m = typeof(Dummy).GetMethod("AnnotatedMethod");
            var p = m.GetParameters()[0];
            Assert.True(p.GetCustomAttributes(typeof(TrackableAttribute), false).Any());
        }

        [Fact]
        public void TestTargetTypeOnAnnotation()
        {
            var ta = typeof(Dummy).GetMethod("AnnotatedMethod").GetCustomAttribute<TrackableAttribute>();
            Assert.NotNull(ta);
            var targetAttr = typeof(TrackableAttribute).GetCustomAttribute<AttributeUsageAttribute>();
            Assert.NotNull(targetAttr);
            // AttributeTargets.Method + AttributeTargets.Parameter
            ((targetAttr.ValidOn & (AttributeTargets.Method | AttributeTargets.Parameter)).Should().NotBe(0));
        }

        [Fact]
        public void TestRetentionPolicy()
        {
            // .NET attribute retention is always runtime when set as [AttributeUsage(..., Inherited = true)]
            var attr = typeof(TrackableAttribute).GetCustomAttribute<AttributeUsageAttribute>();
            Assert.NotNull(attr);
            attr.Inherited.Should().BeTrue();
        }
    }
}