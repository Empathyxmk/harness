using System;
using System.Collections.Generic;
using System.Threading;
using System.Reflection;
using Xunit;
using Remind101ArchExample.Presenters;

namespace Remind101ArchExample.Tests.Original
{
    public class PresenterManagerTests : IDisposable
    {
        private PresenterManager presenterManager;

        public class DummyPresenter : BasePresenter<object, object> { }

        public PresenterManagerTests()
        {
            presenterManager = new PresenterManager(5, 2, TimeSpan.FromSeconds(1));
        }

        public void Dispose()
        {
            // Not needed for test
        }

        [Fact]
        public void TestSaveAndRestorePresenter()
        {
            var bundle = new Dictionary<string, object>();
            var presenter = new DummyPresenter();
            presenterManager.SavePresenter(presenter, bundle);

            var restored = presenterManager.RestorePresenter(bundle);
            Assert.NotNull(restored);
            Assert.Equal(presenter, restored);
        }

        [Fact]
        public void TestRestorePresenterReturnsNullOnSecondRestore()
        {
            var bundle = new Dictionary<string, object>();
            var presenter = new DummyPresenter();
            presenterManager.SavePresenter(presenter, bundle);

            var firstRestore = presenterManager.RestorePresenter(bundle);
            Assert.NotNull(firstRestore);

            var secondRestore = presenterManager.RestorePresenter(bundle);
            Assert.Null(secondRestore);
        }

        [Fact]
        public void TestGetInstanceReturnsSingleton()
        {
            var instance1 = PresenterManager.GetInstance();
            var instance2 = PresenterManager.GetInstance();
            Assert.Same(instance1, instance2);
        }
    }
}