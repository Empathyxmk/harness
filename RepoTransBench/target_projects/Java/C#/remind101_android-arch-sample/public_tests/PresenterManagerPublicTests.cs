using System;
using System.Collections.Generic;
using System.Threading;
using Xunit;
using Remind101ArchExample.Presenters;

namespace Remind101ArchExample.PublicTests
{
    public class PresenterManagerPublicTests
    {
        private PresenterManager presenterManager;

        public class DummyPresenter : BasePresenter<object, object> { }

        public PresenterManagerPublicTests()
        {
            presenterManager = new PresenterManager(8, 3, TimeSpan.FromMinutes(1));
        }

        [Fact]
        public void TestSaveAndRestorePresenterWithDifferentInstance()
        {
            var bundle = new Dictionary<string, object>();
            var presenter = new DummyPresenter();
            presenterManager.SavePresenter(presenter, bundle);

            var restored = presenterManager.RestorePresenter(bundle);
            Assert.NotNull(restored);
            Assert.Equal(presenter, restored);
        }

        [Fact]
        public void TestRestorePresenterReturnsNullAfterRestoreWithDifferentTimings()
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
        public void TestGetInstanceReturnsSameSingletonInstance()
        {
            var instance1 = PresenterManager.GetInstance();
            var instance2 = PresenterManager.GetInstance();
            Assert.Same(instance1, instance2);
        }
    }
}