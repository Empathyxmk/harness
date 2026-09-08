using Xunit;
using Remind101ArchExample.Presenters;

namespace Remind101ArchExample.PublicTests.Presenters
{
    public class BasePresenterPublicTests
    {
        public class DummyPresenter : BasePresenter<string, int> { }

        [Fact]
        public void TestBasePresenterAttachAndDetachViewPublic()
        {
            var presenter = new DummyPresenter();
            string view = "PUBLIC_TEST_VIEW";
            presenter.AttachView(view);
            Assert.True(presenter.IsViewAttached());
            Assert.Equal(view, presenter.GetView());
            presenter.DetachView();
            Assert.False(presenter.IsViewAttached());
            Assert.Null(presenter.GetView());
        }
    }
}