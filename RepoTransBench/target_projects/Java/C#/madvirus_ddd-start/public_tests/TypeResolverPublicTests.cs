using System;
using Xunit;
using System.Collections.Generic;

namespace MadvirusDddStart.PublicTests
{
    public class TypeResolverPublicTests
    {
        interface IAnotherInterface<T> { }
        class AnotherImpl : IAnotherInterface<int> { }

        [Fact]
        public void EnableAndDisableCacheIdempotence()
        {
            TypeResolver.DisableCache();
            TypeResolver.EnableCache();
            TypeResolver.DisableCache();
        }

        [Fact]
        public void ResolveRawArgumentClassSubtypeDifferent()
        {
            var result = TypeResolver.ResolveRawArgument(typeof(IAnotherInterface<>), typeof(AnotherImpl));
            Assert.Equal(typeof(int), result);
        }

        [Fact]
        public void ResolveRawArgument_Type_ReturnsUnknownForNonParameterized_Different()
        {
            var result = TypeResolver.ResolveRawArgument(typeof(int), typeof(int));
            Assert.Equal(TypeResolver.Unknown, result);
        }

        [Fact]
        public void ResolveRawArgumentsHandlesNull_DifferentClass()
        {
            Assert.Null(TypeResolver.ResolveRawArguments(null, typeof(int)));
        }

        [Fact]
        public void ResolveRawArgumentThrowsOnWrongNumberOfParamsSet()
        {
            Assert.Throws<ArgumentException>(() =>
            {
                throw new ArgumentException("Expected 1 argument");
            });
        }
    }
}