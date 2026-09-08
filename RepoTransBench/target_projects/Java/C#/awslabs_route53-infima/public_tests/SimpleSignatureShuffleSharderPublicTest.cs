using System;
using System.Collections.Generic;
using Xunit;

namespace Route53Infima.PublicTests
{
    public class SimpleSignatureShuffleSharderPublicTest
    {
        [Fact]
        public void TestShuffleShardReturnsCorrectSizeWithDifferentData()
        {
            var lattice = new OneDimensionalLattice<string>();
            lattice.AddEndpoints("az2", new List<string> { "W", "X", "Y", "Z" });
            var sharder = new SimpleSignatureShuffleSharder<string>(456L);

            var shard = sharder.ShuffleShard(lattice, System.Text.Encoding.UTF8.GetBytes("unique-777"), 3);
            var endpoints = shard.GetAllEndpoints();
            Assert.Equal(3, endpoints.Count);
        }

        [Fact]
        public void TestShuffleShardDifferentIdentifiersProduceDifferentShardsWithDifferentData()
        {
            var lattice = new OneDimensionalLattice<string>();
            lattice.AddEndpoints("public", new List<string> { "X", "Y", "Z", "W" });
            var sharder = new SimpleSignatureShuffleSharder<string>(99L);

            var shard1 = sharder.ShuffleShard(lattice, System.Text.Encoding.UTF8.GetBytes("alpha"), 2);
            var shard2 = sharder.ShuffleShard(lattice, System.Text.Encoding.UTF8.GetBytes("beta"), 2);

            Assert.NotEqual(new HashSet<string>(shard1.GetAllEndpoints()), new HashSet<string>(shard2.GetAllEndpoints()));
        }

        [Fact]
        public void TestThrowsNoSuchAlgorithmExceptionCoverageOnly()
        {
            // Coverage only, as in Java.
            var sharder = new SimpleSignatureShuffleSharder<string>(13L);
        }
    }
}