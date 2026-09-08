using System;
using Xunit;
using MultipleSourcesSample;

namespace MultipleSourcesSample.PublicTests
{
    public class SourcesPublicTests
    {
        private Sources sources;

        public SourcesPublicTests()
        {
            sources = new Sources();
        }

        [Fact]
        public void TestMemoryInitialNullPublic()
        {
            Data val = null;
            bool completed = false;
            sources.Memory().Subscribe(
                x => val = x,
                () => completed = true
            );
            Assert.Null(val);
            Assert.True(completed);
        }

        [Fact]
        public void TestDiskInitialNullPublic()
        {
            Data val = null;
            bool completed = false;
            sources.Disk().Subscribe(
                x => val = x,
                () => completed = true
            );
            Assert.Null(val);
            Assert.True(completed);
        }

        [Fact]
        public void TestNetworkReturnsDataAndCachesToDiskAndMemoryPublic()
        {
            bool completed = false;
            sources.Network().Subscribe(
                x => { /* ignore for now */ },
                () => completed = true
            );
            // Memory now has data
            int memCount = 0;
            sources.Memory().Subscribe(x => { if (x != null) memCount++; });
            Assert.Equal(1, memCount);
            // Disk now has data
            int diskCount = 0;
            sources.Disk().Subscribe(x => { if (x != null) diskCount++; });
            Assert.Equal(1, diskCount);
            Assert.True(completed);
        }

        [Fact]
        public void TestClearMemoryPublic()
        {
            sources.Network().FirstAsync().Wait();
            sources.ClearMemory();

            Data val = new Data("temp");
            sources.Memory().Subscribe(x => val = x);

            Assert.Null(val);
        }
    }
}