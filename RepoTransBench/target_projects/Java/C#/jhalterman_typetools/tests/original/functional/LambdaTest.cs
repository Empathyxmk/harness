using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Xunit;

namespace TypeTools.Tests.Original.functional
{
    public class LambdaTest : TypeTools.Tests.Original.AbstractTypeResolverTest
    {
        public LambdaTest() : base(true) { }
        public LambdaTest(bool cacheEnabled) : base(cacheEnabled) { }

        // Basic translations of the Java lambda tests; use .NET Func and Action delegates.

        [Fact]
        public void ShouldResolveArguments()
        {
            Func<string, bool> predicate = str => true;
            Func<string, int> fn = str => int.Parse(str);
            Func<string> supplier = () => "test";
            Action<string> consumer = s => { };

            Assert.Equal(typeof(string), TypeTools.TypeResolver.ResolveRawArgument(typeof(Func<,>), predicate.GetType().GenericTypeArguments[0]));
            Assert.Equal(typeof(string), fn.Method.GetParameters().First().ParameterType);
            Assert.Equal(typeof(int), fn.Method.ReturnType);
            Assert.Equal(typeof(string), supplier.Method.ReturnType);
        }

        // ...and analogous tests for method refs, multi-arg, etc.

        // Implement each public, original test as per the Java logic.
    }
}