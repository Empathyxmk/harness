using Xunit;
using Remind101ArchExample.Presenters;
using Remind101ArchExample;

namespace Remind101ArchExample.PublicTests
{
    public class MvpRecyclerAdapterPublicTests
    {
        public class TestModel
        {
            public int Value;
            public TestModel(int value) { Value = value; }
        }

        public class TestPresenter : BasePresenter<TestModel, object> { }

        public class TestViewHolder : MvpViewHolder<TestPresenter>
        {
            public bool Bound = false;
            public bool Unbound = false;
            public TestPresenter LastPresenter = null;
            public TestViewHolder() : base(null) { }

            public override void BindPresenter(TestPresenter presenter)
            {
                Bound = true;
                LastPresenter = presenter;
            }

            public override void UnbindPresenter()
            {
                Unbound = true;
                LastPresenter = null;
            }
        }

        public class TestAdapter : MvpRecyclerAdapter<TestModel, TestPresenter, TestViewHolder>
        {
            private readonly TestModel[] items;
            public TestAdapter(params TestModel[] items)
            {
                this.items = items;
                foreach (var m in items)
                    Presenters[GetModelId(m)] = CreatePresenter(m);
            }

            protected override TestPresenter CreatePresenter(TestModel model) => new TestPresenter();
            protected override object GetModelId(TestModel model) => model.Value;
            protected override TestModel GetItem(int position) => items[position];
        }

        [Fact]
        public void TestBindAndUnbindPresenterWithDifferentModelData()
        {
            var model = new TestModel(100);
            var adapter = new TestAdapter(model);

            var holder = new TestViewHolder();

            adapter.OnBindViewHolder(holder, 0);
            Assert.True(holder.Bound);
            Assert.NotNull(holder.LastPresenter);

            adapter.OnViewRecycled(holder);
            Assert.True(holder.Unbound);
            Assert.Null(holder.LastPresenter);
        }

        [Fact]
        public void TestOnFailedToRecycleViewCallsUnbindWithDifferentModel()
        {
            var model = new TestModel(997);
            var adapter = new TestAdapter(model);

            var holder = new TestViewHolder();

            var result = adapter.OnFailedToRecycleView(holder);
            Assert.True(holder.Unbound);
        }
    }
}