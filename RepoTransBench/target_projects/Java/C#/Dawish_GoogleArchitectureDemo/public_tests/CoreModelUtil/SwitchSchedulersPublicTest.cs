using System;
using Xunit;
using System.Reactive.Linq;
using System.Reactive.Concurrency;

namespace DawishGoogleArchitectureDemo.PublicTests.CoreModelUtil
{
    public class SwitchSchedulersPublicTest
    {
        [Fact]
        public void ApplySchedulers_DifferentData()
        {
            // Use System.Reactive's ImmediateScheduler for testing threading
            var observable = Observable.Return("alpha");
            string received = null;
            observable.ObserveOn(ImmediateScheduler.Instance)
                      .SubscribeOn(ImmediateScheduler.Instance)
                      .Subscribe(v => received = v);

            Assert.Equal("alpha", received);
        }
    }
}