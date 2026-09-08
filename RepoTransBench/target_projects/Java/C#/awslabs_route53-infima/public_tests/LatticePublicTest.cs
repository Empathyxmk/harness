using System;
using System.Collections.Generic;
using Xunit;

namespace Route53Infima.PublicTests
{
    public class LatticePublicTest
    {
        [Fact]
        public void TestConstructionAndDimensionNamesWithDifferentDims()
        {
            var dims = new List<string> { "dimA", "dimB" };
            var lattice = new Lattice<int>(dims);
            Assert.Equal(dims, lattice.GetDimensionNames());
        }

        [Fact]
        public void TestAddEndpointsForSectorAndGetEndpointsDifferent()
        {
            var lattice = new Lattice<string>(new List<string> { "y" });
            var coord = new List<string> { "custom" };
            lattice.AddEndpointsForSector(coord, new List<string> { "P", "Q" });
            var endpoints = lattice.GetEndpointsForSector(coord);
            Assert.Contains("P", endpoints);
            Assert.Contains("Q", endpoints);
        }

        [Fact]
        public void TestSimulateFailureDifferentValues()
        {
            var lattice = new Lattice<string>(new List<string> { "country", "city" });
            var coord = new List<string> { "Spain", "Madrid" };
            lattice.AddEndpointsForSector(coord, new List<string> { "Server1", "Server2" });

            var failed = lattice.SimulateFailure("country", "Spain");
            Assert.True(failed.GetAllEndpoints().Count == 0 ||
                        failed.GetEndpointsForSector(coord).Count == 0);
        }

        [Fact]
        public void TestGetDimensionValuesAndDimensionalityPublic()
        {
            var lattice = new Lattice<string>(new List<string> { "continent", "region" });
            lattice.AddEndpointsForSector(new List<string> { "Europe", "North" }, new List<string> { "HostA" });
            lattice.AddEndpointsForSector(new List<string> { "Europe", "South" }, new List<string> { "HostB" });

            var regions = new HashSet<string>(lattice.GetDimensionValues("region"));
            Assert.Contains("North", regions);
            Assert.Contains("South", regions);

            var dims = lattice.GetDimensionality();
            Assert.Equal(2, dims.Count);
        }

        [Fact]
        public void TestEqualsAndHashCodeDifferentData()
        {
            var l1 = new Lattice<string>(new List<string> { "R", "S" });
            var l2 = new Lattice<string>(new List<string> { "R", "S" });
            l1.AddEndpointsForSector(new List<string> { "foo", "bar" }, new List<string> { "baz" });
            l2.AddEndpointsForSector(new List<string> { "foo", "bar" }, new List<string> { "baz" });
            Assert.Equal(l1, l2);
            Assert.Equal(l1.GetHashCode(), l2.GetHashCode());
        }

        [Fact]
        public void TestToStringNotNullPublic()
        {
            var lattice = new Lattice<string>(new List<string> { "E" });
            Assert.NotNull(lattice.ToString());
        }

        [Fact]
        public void TestNoEndpointsPublic()
        {
            var lattice = new Lattice<string>(new List<string> { "F" });
            Assert.Empty(lattice.GetAllEndpoints());
        }
    }
}