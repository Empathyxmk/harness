using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.Support.MouseMotion;

namespace JoonasVali.NaturalMouseMotion.PublicTests.Support.MouseMotion
{
    public class DefaultOvershootManagerPublicTest
    {
        [Fact]
        public void ShouldSetOvershootAmount()
        {
            var manager = new DefaultOvershootManager();
            manager.SetOvershoots(2);
            Assert.Equal(2, manager.Overshoots.Count);
        }
    }
}