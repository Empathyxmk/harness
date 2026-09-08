using Xunit;
using Remind101ArchExample.Presenters;

namespace Remind101ArchExample.Tests.Original.Presenters
{
    public class BasePresenterTests
    {
        public class DummyView { }

        public class DummyPresenter : BasePresenter<DummyView, object> { }

        [Fact]
        public void TestBindViewAndUnbindView()
        {
            var presenter = new DummyPresenter();
            var view = new DummyView();
            presenter.BindView(view);
            Assert.NotNull(presenter.GetView());

            presenter.UnbindView();
            Assert.Null(presenter.GetView());
        }
    }
}