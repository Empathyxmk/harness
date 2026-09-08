using System.Reflection;
using Xunit;

namespace Orhanobut.Tracklytics.PublicTests
{
    public class TrackableAttributeAnnotationPublicTest
    {
        [TrackableAttribute(Key = "username", Value = "testUser")]
        public void Sample([TrackableAttribute(Key = "country", Value = "US")] string country) { }

        [Fact]
        public void TestTrackableAttributeAnnotationOnMethodPublic()
        {
            var method = GetType().GetMethod("Sample", new[] { typeof(string) });
            var ta = method.GetCustomAttribute<TrackableAttribute>();
            Assert.Equal("username", ta.Key);
            Assert.Equal("testUser", ta.Value);
        }

        [Fact]
        public void TestTrackableAttributeAnnotationOnParameterPublic()
        {
            var method = GetType().GetMethod("Sample", new[] { typeof(string) });
            var ta = (TrackableAttribute)method.GetParameters()[0].GetCustomAttribute(typeof(TrackableAttribute), false);
            Assert.Equal("country", ta.Key);
            Assert.Equal("US", ta.Value);
        }
    }
}