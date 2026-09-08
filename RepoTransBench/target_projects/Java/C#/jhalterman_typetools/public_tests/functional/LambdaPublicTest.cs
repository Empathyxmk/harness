using System;
using System.Collections.Generic;
using Xunit;

namespace TypeTools.Tests.Public.functional
{
    public class LambdaPublicTest
    {
        [Fact]
        public void LambdaTypeResolution_IntegerToDouble()
        {
            Func<int, double> f = i => i;
            var args = TypeTools.TypeResolver.ResolveRawArguments(typeof(Func<,>), f.GetType());
            Assert.Equal(typeof(int), args[0]);
            Assert.Equal(typeof(double), args[1]);
        }

        [Fact]
        public void LambdaTypeResolution_StringToString()
        {
            Func<string, string> f = s => s;
            var args = TypeTools.TypeResolver.ResolveRawArguments(typeof(Func<,>), f.GetType());
            Assert.Equal(typeof(string), args[0]);
            Assert.Equal(typeof(string), args[1]);
        }
    }
}