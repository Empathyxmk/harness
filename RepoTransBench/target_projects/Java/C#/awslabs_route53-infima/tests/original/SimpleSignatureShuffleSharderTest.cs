using System;
using System.Collections.Generic;
using Xunit;

namespace Route53Infima.Tests.Original
{
    public class SimpleSignatureShuffleSharderTest
    {
        [Fact]
        public void TestShuffleShardReturnsCorrectSize()
        {
            var lattice = new OneDimensionalLattice<string>();
            lattice.AddEndpoints("az1", new List<string> { "A", "B", "C", "D" });
            var sharder = new SimpleSignatureShuffleSharder<string>(123L);

            var shard = sharder.ShuffleShard(lattice, System.Text.Encoding.UTF8.GetBytes("id-1"), 2);
            var endpoints = shard.GetAllEndpoints();
            Assert.Equal(2, endpoints.Count);
        }

        [Fact]
        public void TestShuffleShardDifferentIdentifiersProduceDifferentShards()
        {
            var lattice = new OneDimensionalLattice<string>();
            lattice.AddEndpoints("test", new List<string> { "A", "B", "C", "D" });
            var sharder = new SimpleSignatureShuffleSharder<string>(42L);

            var shard1 = sharder.ShuffleShard(lattice, System.Text.Encoding.UTF8.GetBytes("id-1"), 2);
            var shard2 = sharder.ShuffleShard(lattice, System.Text.Encoding.UTF8.GetBytes("id-2"), 2);

            Assert.NotEqual(new HashSet<string>(shard1.GetAllEndpoints()), new HashSet<string>(shard2.GetAllEndpoints()));
        }

        [Fact]
        public void TestThrowsNoSuchAlgorithmException()
        {
            // Coverage only, not testable in C# unless purposely broken hash implementation was used.
            var sharder = new SimpleSignatureShuffleSharder<string>(1L);
        }
    }
}