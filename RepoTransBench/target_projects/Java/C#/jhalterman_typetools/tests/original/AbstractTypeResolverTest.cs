using System;
using Xunit;

namespace TypeTools.Tests.Original
{
    // Abstract base for tests. In C# xUnit we cannot use abstract [Fact] methods,
    // so we refactor cache setup to a base class method, and let derived
    // tests opt-in by calling the SetupCache() method.
    public abstract class AbstractTypeResolverTest
    {
        protected readonly bool cacheEnabled;

        protected AbstractTypeResolverTest(bool cacheEnabled)
        {
            this.cacheEnabled = cacheEnabled;
            SetCache();
        }

        protected void SetCache()
        {
            if (cacheEnabled)
                TypeTools.TypeResolver.EnableCache();
            else
                TypeTools.TypeResolver.DisableCache();
        }
    }
}