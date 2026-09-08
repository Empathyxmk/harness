using Xunit;
using Remind101ArchExample.Presenters;
using Remind101ArchExample;

namespace Remind101ArchExample.Tests.Original
{
    public class MvpViewHolderTests
    {
        public class DummyPresenter : BasePresenter<DummyViewHolder, object>
        {
            public bool WasBind = false;

            public override void BindView(DummyViewHolder view)
            {
                WasBind = true;
            }
        }

        public class DummyViewHolder : MvpViewHolder<DummyPresenter>
        {
            public DummyViewHolder() : base(null) { }
        }

        [Fact]
        public void TestBindAndUnbindPresenter()
        {
            var presenter = new DummyPresenter();
            var vh = new DummyViewHolder();

            vh.BindPresenter(presenter);
            Assert.Equal(presenter, vh.Presenter);
            Assert.True(presenter.WasBind);

            vh.UnbindPresenter();
            Assert.Null(vh.Presenter);
        }
    }
}