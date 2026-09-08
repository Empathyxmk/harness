using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.Support.MouseMotion;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.Support.MouseMotion
{
    public class DefaultOvershootManagerTest
    {
        [Fact]
        public void ShouldInitializeOvershootManagerProperly()
        {
            var manager = new DefaultOvershootManager();
            Assert.NotNull(manager);
            Assert.True(manager.Overshoots.Count >= 0);
        }
    }
}