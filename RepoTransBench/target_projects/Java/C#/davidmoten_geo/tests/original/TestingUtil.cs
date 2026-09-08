using System;
using System.Reflection;
using Xunit;

namespace DavidMoten.Geo.Tests
{
    /// <summary>
    /// Utility methods for unit tests.
    /// </summary>
    public static class TestingUtil
    {
        /// <summary>
        /// Checks that a class has a no-argument private constructor and calls that constructor to instantiate the class.
        /// </summary>
        public static void CallConstructorAndCheckIsPrivate(Type type)
        {
            ConstructorInfo ctor = type.GetConstructor(BindingFlags.NonPublic | BindingFlags.Instance, null, Type.EmptyTypes, null);
            Assert.NotNull(ctor);
            Assert.True(ctor.IsPrivate, "Constructor is not private.");
            var obj = ctor.Invoke(null);
            Assert.NotNull(obj);
        }
    }
}