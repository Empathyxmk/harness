using System;
using System.Reactive.Linq;
using Xunit;
using MultipleSourcesSample;

namespace MultipleSourcesSample.Tests
{
    public class SourcesBranchTests
    {
        private Sources sources;

        public SourcesBranchTests()
        {
            sources = new Sources();
        }

        [Fact]
        public void TestMemoryWithFreshData()
        {
            // Put data in memory (via network)
            sources.Network().FirstAsync().Wait();
            Data result = null;
            sources.Memory().Subscribe(d => result = d);
            Assert.NotNull(result);
        }

        [Fact]
        public void TestDiskWithFreshData()
        {
            sources.Network().FirstAsync().Wait();
            Data result = null;
            sources.Disk().Subscribe(d => result = d);
            Assert.NotNull(result);
        }

        [Fact]
        public void TestNetworkMultipleRequests()
        {
            var data1 = sources.Network().FirstAsync().Wait();
            var data2 = sources.Network().FirstAsync().Wait();
            Data result = null;
            sources.Memory().Subscribe(d => result = d);
            Assert.NotNull(result);
            Assert.NotEqual(data1.value, data2.value);
        }

        [Fact]
        public void TestLogSourceNullAndStale()
        {
            var subject = new System.Reactive.Subjects.ReplaySubject<Data>();

            subject.OnNext(null);
            var staleData = new Data("x");
            staleData.IsUpToDateOverride = () => false;
            subject.OnNext(staleData);

            var freshData = new Data("y");
            freshData.IsUpToDateOverride = () => true;
            subject.OnNext(freshData);

            subject.OnCompleted();

            int count = 0;
            subject.AsObservable()
                .Let(sources.LogSource("UNITTEST"))
                .Subscribe(d => count++);

            Assert.Equal(3, count);
        }
    }
}