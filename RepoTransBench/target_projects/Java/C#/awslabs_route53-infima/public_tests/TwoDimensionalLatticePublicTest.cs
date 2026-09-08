using System;
using System.Collections.Generic;
using Xunit;

namespace Route53Infima.PublicTests
{
    public class TwoDimensionalLatticePublicTest
    {
        [Fact]
        public void TestAddAndGetEndpointsDifferentData()
        {
            var lattice = new TwoDimensionalLattice<string>("rack", "slot");
            lattice.AddEndpoints("rack-17", "slot-9", new List<string> { "R", "S", "T" });
            var found = lattice.GetEndpoints("rack-17", "slot-9");
            Assert.Contains("R", found);
            Assert.Contains("S", found);
            Assert.Contains("T", found);
        }

        [Fact]
        public void TestAddEndpointDifferentData()
        {
            var lattice = new TwoDimensionalLattice<string>("zoneA", "rowB");
            lattice.AddEndpoint("foo", "bar", "X");
            var found = lattice.GetEndpoints("foo", "bar");
            Assert.Contains("X", found);
            Assert.Single(found);
        }

        [Fact]
        public void TestGetEndpointsForNonexistentCoordinatesPublic()
        {
            var lattice = new TwoDimensionalLattice<string>("c", "d");
            Assert.Empty(lattice.GetEndpoints("doesnot", "exist"));
        }

        [Fact]
        public void TestDimensionNamesPublic()
        {
            var lattice = new TwoDimensionalLattice<string>("fruit", "color");
            Assert.Equal(new List<string> { "fruit", "color" }, lattice.GetDimensionNames());
        }
    }
}