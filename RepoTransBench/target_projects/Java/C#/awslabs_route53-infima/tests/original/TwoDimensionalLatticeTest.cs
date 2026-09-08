using System;
using System.Collections.Generic;
using Xunit;

namespace Route53Infima.Tests.Original
{
    public class TwoDimensionalLatticeTest
    {
        [Fact]
        public void TestConstructorAndDimensionNames()
        {
            var lattice = new TwoDimensionalLattice<string>("D1", "D2");
            Assert.Equal(new List<string> { "D1", "D2" }, lattice.GetDimensionNames());
        }

        [Fact]
        public void TestAddEndpointsAndGetEndpoints()
        {
            var lattice = new TwoDimensionalLattice<string>("X", "Y");
            lattice.AddEndpoints("a", "b", new List<string> { "foo", "bar" });
            var got = lattice.GetEndpoints("a", "b");
            Assert.Contains("foo", got);
            Assert.Contains("bar", got);
        }

        [Fact]
        public void TestAddEndpoint()
        {
            var lattice = new TwoDimensionalLattice<string>("A", "B");
            lattice.AddEndpoint("X", "Y", "Z");
            var got = lattice.GetEndpoints("X", "Y");
            Assert.Single(got);
            Assert.Contains("Z", got);
        }

        [Fact]
        public void TestGetEndpointsNotPresent()
        {
            var lattice = new TwoDimensionalLattice<string>("DD1", "DD2");
            Assert.Empty(lattice.GetEndpoints("no", "key"));
        }
    }
}