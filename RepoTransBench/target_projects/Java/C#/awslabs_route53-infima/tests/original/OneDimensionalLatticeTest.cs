using System;
using System.Collections.Generic;
using Xunit;

namespace Route53Infima.Tests.Original
{
    public class OneDimensionalLatticeTest
    {
        [Fact]
        public void TestConstructorWithName()
        {
            var lattice = new OneDimensionalLattice<string>("Zone");
            Assert.NotNull(lattice);
            Assert.Equal(new List<string> { "Zone" }, lattice.GetDimensionNames());
        }

        [Fact]
        public void TestDefaultConstructor()
        {
            var lattice = new OneDimensionalLattice<string>();
            Assert.NotNull(lattice);
            Assert.Equal(new List<string> { "AvailabilityZone" }, lattice.GetDimensionNames());
        }

        [Fact]
        public void TestAddAndGetEndpoints()
        {
            var lattice = new OneDimensionalLattice<string>();
            lattice.AddEndpoints("us-east-1a", new List<string> { "A", "B" });
            var result = lattice.GetEndpoints("us-east-1a");
            Assert.Contains("A", result);
            Assert.Contains("B", result);
        }

        [Fact]
        public void TestAddEndpoint()
        {
            var lattice = new OneDimensionalLattice<string>();
            lattice.AddEndpoint("us-west-2", "Foo");
            var res = lattice.GetEndpoints("us-west-2");
            Assert.Single(res);
            Assert.Contains("Foo", res);
        }

        [Fact]
        public void TestEmptyEndpoints()
        {
            var lattice = new OneDimensionalLattice<string>();
            Assert.Empty(lattice.GetEndpoints("nonexistent"));
        }
    }
}