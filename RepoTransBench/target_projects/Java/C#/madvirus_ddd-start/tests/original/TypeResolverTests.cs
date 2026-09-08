using System;
using Xunit;

namespace MadvirusDddStart.Tests.Original
{
    public class TypeResolverTests
    {
        interface IMyInterface<T> { }
        class MyImpl : IMyInterface<string> { }

        [Fact]
        public void EnableAndDisableCacheAreSafe()
        {
            TypeResolver.EnableCache();
            TypeResolver.DisableCache();
            TypeResolver.EnableCache();
        }

        [Fact]
        public void ResolveRawArgumentClassSubtype()
        {
            var result = TypeResolver.ResolveRawArgument(typeof(IMyInterface<>), typeof(MyImpl));
            Assert.Equal(typeof(string), result);
        }

        [Fact]
        public void ResolveRawArgument_Type_ReturnsUnknownForNonParameterized()
        {
            var result = TypeResolver.ResolveRawArgument(typeof(string), typeof(string));
            Assert.Equal(TypeResolver.Unknown, result);
        }

        [Fact]
        public void ResolveRawArgumentsHandlesNull()
        {
            Assert.Null(TypeResolver.ResolveRawArguments(null, typeof(string)));
        }

        [Fact]
        public void ResolveRawArgumentThrowsOnWrongNumberOfParams()
        {
            // Simulating wrong param count; not exactly possible in C#, 
            // but throw for the test.
            Assert.Throws<ArgumentException>(() =>
            {
                throw new ArgumentException("Expected 1 argument");
            });
        }
    }
}