using System;
using System.Collections.Generic;
using Xunit;

namespace Route53Infima.Tests.Original
{
    public class LatticeTest
    {
        [Fact]
        public void TestConstructionAndDimensionNames()
        {
            var dims = new List<string> { "x", "y" };
            var lattice = new Lattice<int>(dims);
            Assert.Equal(dims, lattice.GetDimensionNames());
        }

        [Fact]
        public void TestAddEndpointsForSectorAndGetEndpoints()
        {
            var lattice = new Lattice<string>(new List<string> { "x" });
            var coord = new List<string> { "test" };
            lattice.AddEndpointsForSector(coord, new List<string> { "A", "B" });
            var endpoints = lattice.GetEndpointsForSector(coord);
            Assert.Contains("A", endpoints);
            Assert.Contains("B", endpoints);
        }

        [Fact]
        public void TestSimulateFailure()
        {
            var lattice = new Lattice<string>(new List<string> { "X", "Y" });
            var coord1 = new List<string> { "A", "B" };
            lattice.AddEndpointsForSector(coord1, new List<string> { "E1", "E2" });

            var failed = lattice.SimulateFailure("X", "A");
            // Should remove coordinates where X == "A"
            Assert.True(failed.GetAllEndpoints().Count == 0 ||
                        failed.GetEndpointsForSector(coord1).Count == 0);
        }

        [Fact]
        public void TestGetDimensionValuesAndDimensionality()
        {
            var lattice = new Lattice<string>(new List<string> { "X", "Y" });
            lattice.AddEndpointsForSector(new List<string> { "A", "B" }, new List<string> { "Z" });
            lattice.AddEndpointsForSector(new List<string> { "A", "C" }, new List<string> { "Q" });

            var yvals = new HashSet<string>(lattice.GetDimensionValues("Y"));
            Assert.Contains("B", yvals);
            Assert.Contains("C", yvals);

            var dims = lattice.GetDimensionality();
            Assert.Equal(2, dims.Count);
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var l1 = new Lattice<string>(new List<string> { "X", "Y" });
            var l2 = new Lattice<string>(new List<string> { "X", "Y" });
            l1.AddEndpointsForSector(new List<string> { "A", "B" }, new List<string> { "Q" });
            l2.AddEndpointsForSector(new List<string> { "A", "B" }, new List<string> { "Q" });
            Assert.Equal(l1, l2);
            Assert.Equal(l1.GetHashCode(), l2.GetHashCode());
        }

        [Fact]
        public void TestToStringNotNull()
        {
            var lattice = new Lattice<string>(new List<string> { "D" });
            Assert.NotNull(lattice.ToString());
        }

        [Fact]
        public void TestNoEndpoints()
        {
            var lattice = new Lattice<string>(new List<string> { "D" });
            Assert.Empty(lattice.GetAllEndpoints());
        }
    }
}