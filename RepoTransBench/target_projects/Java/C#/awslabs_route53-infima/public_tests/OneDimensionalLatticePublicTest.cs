using System;
using System.Collections.Generic;
using Xunit;

namespace Route53Infima.PublicTests
{
    public class OneDimensionalLatticePublicTest
    {
        [Fact]
        public void TestConstructorWithNameDifferent()
        {
            var lattice = new OneDimensionalLattice<string>("ZoneX");
            Assert.NotNull(lattice);
            Assert.Equal(new List<string> { "ZoneX" }, lattice.GetDimensionNames());
        }

        [Fact]
        public void TestDefaultConstructorPublic()
        {
            var lattice = new OneDimensionalLattice<string>();
            Assert.NotNull(lattice);
            Assert.Equal(new List<string> { "AvailabilityZone" }, lattice.GetDimensionNames());
        }

        [Fact]
        public void TestAddAndGetEndpointsDifferentData()
        {
            var lattice = new OneDimensionalLattice<string>();
            lattice.AddEndpoints("eu-central-1b", new List<string> { "M", "N" });
            var result = lattice.GetEndpoints("eu-central-1b");
            Assert.Contains("M", result);
            Assert.Contains("N", result);
        }

        [Fact]
        public void TestAddEndpointDifferentData()
        {
            var lattice = new OneDimensionalLattice<string>();
            lattice.AddEndpoint("eu-north-1", "Bar");
            var res = lattice.GetEndpoints("eu-north-1");
            Assert.Single(res);
            Assert.Contains("Bar", res);
        }

        [Fact]
        public void TestEmptyEndpointsPublic()
        {
            var lattice = new OneDimensionalLattice<string>();
            Assert.Empty(lattice.GetEndpoints("doesnotexist"));
        }
    }
}