using Xunit;
using Remind101ArchExample.Presenters;
using Remind101ArchExample.Models;
using Remind101ArchExample.Views;

namespace Remind101ArchExample.PublicTests.Presenters
{
    public class CounterPresenterPublicTests
    {
        private CounterPresenter presenter;
        private Counter counter;

        public class DummyView : ICounterView
        {
            public int LastValue = -1;
            public bool OnIncrement = false;
            public bool OnDecrement = false;

            public void SetValue(int value)
            {
                LastValue = value;
            }

            public void ShowIncremented()
            {
                OnIncrement = true;
            }

            public void ShowDecremented()
            {
                OnDecrement = true;
            }
        }

        public CounterPresenterPublicTests()
        {
            counter = new Counter();
            counter.SetValue(42);
            presenter = new CounterPresenter(counter);
        }

        [Fact]
        public void TestIncrementPublic()
        {
            var view = new DummyView();
            presenter.AttachView(view);

            presenter.Increment();
            Assert.Equal(43, counter.GetValue());
            Assert.Equal(43, view.LastValue);
            Assert.True(view.OnIncrement);
        }

        [Fact]
        public void TestDecrementPublic()
        {
            var view = new DummyView();
            presenter.AttachView(view);

            presenter.Decrement();
            Assert.Equal(41, counter.GetValue());
            Assert.Equal(41, view.LastValue);
            Assert.True(view.OnDecrement);
        }

        [Fact]
        public void TestAttachDetachViewPublic()
        {
            var view = new DummyView();
            presenter.AttachView(view);
            Assert.True(presenter.IsViewAttached());
            presenter.DetachView();
            Assert.False(presenter.IsViewAttached());
        }
    }
}