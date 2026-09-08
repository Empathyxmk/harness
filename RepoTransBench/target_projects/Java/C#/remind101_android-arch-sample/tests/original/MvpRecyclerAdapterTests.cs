using Xunit;
using Remind101ArchExample.Presenters;
using Remind101ArchExample;

namespace Remind101ArchExample.Tests.Original
{
    public class MvpRecyclerAdapterTests
    {
        public class DummyModel
        {
            public int Id;
            public DummyModel(int id) { Id = id; }
        }

        public class DummyPresenter : BasePresenter<DummyViewHolder, DummyModel> { }

        public class DummyViewHolder : MvpViewHolder<DummyPresenter>
        {
            public bool WasBound = false;
            public bool WasUnbound = false;

            public DummyViewHolder() : base(null) { }

            public override void BindPresenter(DummyPresenter presenter)
            {
                base.BindPresenter(presenter);
                WasBound = true;
            }

            public override void UnbindPresenter()
            {
                WasUnbound = true;
                base.UnbindPresenter();
            }
        }

        public class DummyAdapter : MvpRecyclerAdapter<DummyModel, DummyPresenter, DummyViewHolder>
        {
            public DummyModel[] Models = new DummyModel[] { new DummyModel(1), new DummyModel(2) };

            public DummyAdapter()
            {
                foreach (var m in Models)
                {
                    Presenters[m.Id] = CreatePresenter(m);
                }
            }

            protected override DummyPresenter CreatePresenter(DummyModel model) => new DummyPresenter();
            protected override object GetModelId(DummyModel model) => model.Id;
            protected override DummyModel GetItem(int position) => Models[position];
            public override int GetItemCount() => Models.Length;
        }

        private DummyAdapter adapter;

        public MvpRecyclerAdapterTests()
        {
            adapter = new DummyAdapter();
        }

        [Fact]
        public void TestGetPresenterReturnsCorrectPresenter()
        {
            var m = new DummyModel(1);
            var p = adapter.GetPresenter(m);
            Assert.NotNull(p);
        }

        [Fact]
        public void TestOnBindViewHolderBindsPresenter()
        {
            var holder = new DummyViewHolder();
            adapter.OnBindViewHolder(holder, 0);
            Assert.True(holder.WasBound);
        }

        [Fact]
        public void TestOnViewRecycledUnbindsPresenter()
        {
            var holder = new DummyViewHolder();
            adapter.OnViewRecycled(holder);
            Assert.True(holder.WasUnbound);
        }

        [Fact]
        public void TestOnFailedToRecycleViewUnbindsPresenter()
        {
            var holder = new DummyViewHolder();
            var returned = adapter.OnFailedToRecycleView(holder);
            Assert.True(holder.WasUnbound);
            Assert.False(returned);
        }
    }
}