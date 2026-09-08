using Xunit;
using System;

namespace Feather.Tests
{
    public class CircularDependencyTest
    {
        [Fact]
        public void CircularDependencyCaught()
        {
            var feather = FeatherBase.With();
            Assert.Throws<FeatherException>(() => feather.Instance(typeof(Circle1)));
        }

        [Fact]
        public void CircularDependencyWithProviderAllowed()
        {
            var feather = FeatherBase.With();
            var circle1 = (CircleWithProvider1)feather.Instance(typeof(CircleWithProvider1));
            Assert.NotNull(circle1.CircleWithProvider2.CircleWithProvider1.Get());
        }

        public class Circle1
        {
            public Circle2 Circle2 { get; }
            public Circle1(Circle2 circle2) => Circle2 = circle2;
        }
        public class Circle2
        {
            public Circle1 Circle1 { get; }
            public Circle2(Circle1 circle1) => Circle1 = circle1;
        }
        public class CircleWithProvider1
        {
            public CircleWithProvider2 CircleWithProvider2 { get; }
            public CircleWithProvider1(CircleWithProvider2 circleWithProvider2) => CircleWithProvider2 = circleWithProvider2;
        }
        public class CircleWithProvider2
        {
            public IProvider<CircleWithProvider1> CircleWithProvider1 { get; }
            public CircleWithProvider2(IProvider<CircleWithProvider1> circleWithProvider1) => CircleWithProvider1 = circleWithProvider1;
        }
    }
}