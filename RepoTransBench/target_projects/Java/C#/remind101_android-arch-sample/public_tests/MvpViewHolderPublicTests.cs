using Xunit;
using Remind101ArchExample.Presenters;
using Remind101ArchExample;

namespace Remind101ArchExample.PublicTests
{
    public class MvpViewHolderPublicTests
    {
        public class DummyPresenter : BasePresenter<string, object> { }

        public class DummyViewHolder : MvpViewHolder<DummyPresenter>
        {
            public bool BindCalled = false;
            public bool UnbindCalled = false;
            public DummyPresenter BoundPresenter = null;

            public DummyViewHolder() : base(null) { }

            public override void BindPresenter(DummyPresenter presenter)
            {
                BindCalled = true;
                BoundPresenter = presenter;
            }

            public override void UnbindPresenter()
            {
                UnbindCalled = true;
                BoundPresenter = null;
            }
        }

        [Fact]
        public void TestBindAndUnbindPresenterPublic()
        {
            var presenter = new DummyPresenter();
            var viewHolder = new DummyViewHolder();

            viewHolder.BindPresenter(presenter);
            Assert.True(viewHolder.BindCalled);
            Assert.Equal(presenter, viewHolder.BoundPresenter);

            viewHolder.UnbindPresenter();
            Assert.True(viewHolder.UnbindCalled);
            Assert.Null(viewHolder.BoundPresenter);
        }
    }
}