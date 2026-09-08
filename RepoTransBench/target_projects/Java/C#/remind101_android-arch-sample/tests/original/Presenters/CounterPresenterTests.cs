using Xunit;
using Remind101ArchExample.Presenters;
using Remind101ArchExample.Models;
using Moq;
using Remind101ArchExample.Views;

namespace Remind101ArchExample.Tests.Original.Presenters
{
    public class CounterPresenterTests
    {
        private CounterPresenter presenter;
        private Mock<ICounterView> view;
        private Counter counter;

        public CounterPresenterTests()
        {
            presenter = new CounterPresenter();
            view = new Mock<ICounterView>();
            presenter.BindView(view.Object);
            counter = new Counter();
            counter.SetId(4);
            counter.SetName("My Counter");
            counter.SetValue(18);
        }

        [Fact]
        public void TestUpdateViewSetsName()
        {
            presenter.SetModel(counter);

            view.Verify(v => v.SetCounterName("My Counter"));
        }

        [Fact]
        public void TestUpdateViewSetsValue()
        {
            presenter.SetModel(counter);

            view.Verify(v => v.SetCounterValue(18));
        }

        [Fact]
        public void TestUpdateViewSetsMinusButtonEnabled()
        {
            presenter.SetModel(counter);

            view.Verify(v => v.SetMinusButtonEnabled(true));
        }

        [Fact]
        public void TestUpdateViewWhenCounterEqual0SetsMinusButtonDisabled()
        {
            counter.SetValue(0);
            presenter.SetModel(counter);

            view.Verify(v => v.SetMinusButtonEnabled(false));
        }

        [Fact]
        public void TestUpdateViewWhenCounterLowerThan99SetsPlusButtonEnabled()
        {
            presenter.SetModel(counter);

            view.Verify(v => v.SetPlusButtonEnabled(true));
        }

        [Fact]
        public void TestUpdateViewWhenCounterEqual99SetsMinusButtonDisabled()
        {
            counter.SetValue(99);
            presenter.SetModel(counter);

            view.Verify(v => v.SetPlusButtonEnabled(false));
        }

        [Fact]
        public void TestOnMinusButtonClickedWhenCounterGreaterThan0DecrementsValue()
        {
            counter.SetValue(16);
            presenter.SetModel(counter);
            view.Invocations.Clear();

            presenter.OnMinusButtonClicked();
            Assert.Equal(15, counter.GetValue());
        }

        [Fact]
        public void TestOnMinusButtonClickedWhenCounterEquals0DoesNotDoAnything()
        {
            counter.SetValue(0);
            presenter.SetModel(counter);
            view.Invocations.Clear();

            presenter.OnMinusButtonClicked();
            Assert.Equal(0, counter.GetValue());
        }

        [Fact]
        public void TestOnPlusButtonClickedWhenCounterLowerThan99IncrementsValue()
        {
            counter.SetValue(16);
            presenter.SetModel(counter);
            view.Invocations.Clear();

            presenter.OnPlusButtonClicked();
            Assert.Equal(17, counter.GetValue());
        }

        [Fact]
        public void TestOnPlusButtonClickedWhenCounterEquals99DoesNotDoAnything()
        {
            counter.SetValue(99);
            presenter.SetModel(counter);
            view.Invocations.Clear();

            presenter.OnPlusButtonClicked();
            Assert.Equal(99, counter.GetValue());
        }

        [Fact]
        public void TestOnCounterClickedOpensDetailView()
        {
            presenter.SetModel(counter);
            view.Invocations.Clear();

            presenter.OnCounterClicked();
            view.Verify(v => v.GoToDetailView(counter));
        }
    }
}