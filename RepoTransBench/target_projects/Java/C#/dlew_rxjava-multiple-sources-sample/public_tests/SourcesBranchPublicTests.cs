using System;
using System.Reactive.Linq;
using Xunit;
using MultipleSourcesSample;

namespace MultipleSourcesSample.PublicTests
{
    public class SourcesBranchPublicTests
    {
        private Sources sources;

        public SourcesBranchPublicTests()
        {
            sources = new Sources();
        }

        [Fact]
        public void TestMemoryWithFreshDataPublic()
        {
            sources.Network().FirstAsync().Wait();
            Data result = null;
            sources.Memory().Subscribe(d => result = d);
            Assert.NotNull(result);
        }

        [Fact]
        public void TestDiskWithFreshDataPublic()
        {
            sources.Network().FirstAsync().Wait();
            Data result = null;
            sources.Disk().Subscribe(d => result = d);
            Assert.NotNull(result);
        }

        [Fact]
        public void TestNetworkMultipleRequestsPublic()
        {
            var dataA = sources.Network().FirstAsync().Wait();
            var dataB = sources.Network().FirstAsync().Wait();
            Data result = null;
            sources.Memory().Subscribe(d => result = d);
            Assert.NotNull(result);
            Assert.NotEqual(dataA.value, dataB.value);
        }

        [Fact]
        public void TestLogSourceNullAndStalePublic()
        {
            var subject = new System.Reactive.Subjects.ReplaySubject<Data>();

            subject.OnNext(null);

            var stale = new Data("abc");
            stale.IsUpToDateOverride = () => false;
            subject.OnNext(stale);

            var fresh = new Data("def");
            fresh.IsUpToDateOverride = () => true;
            subject.OnNext(fresh);

            subject.OnCompleted();

            int count = 0;
            subject.AsObservable()
                .Let(sources.LogSource("UNITTEST_PUBLIC"))
                .Subscribe(d => count++);

            Assert.Equal(3, count);
        }
    }
}