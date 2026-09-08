using System.Collections.Generic;
using Xunit;
using Moq;
using MarkZhai.DataBindingAdapter;

namespace MarkZhai.DataBindingAdapter.Tests.Original
{
    public class BaseViewAdapterTest
    {
        private TestAdapter adapter;
        private object context;
        private object inflater;

        public class TestAdapter : BaseViewAdapter<string>
        {
            public TestAdapter(object c)
            {
                mCollection = new List<string>();
            }
            public override BindingViewHolder<object> OnCreateViewHolder(object parent, int viewType) => null;
            public override void OnBindViewHolder(BindingViewHolder<object> holder, int position) { }
        }

        public BaseViewAdapterTest()
        {
            context = new object();
            inflater = new object();
            adapter = new TestAdapter(context);
            adapter.mCollection.AddRange(new List<string> { "a", "b", "c" });
        }

        [Fact]
        public void TestRemove()
        {
            adapter.Remove(1);
            Assert.Equal(2, adapter.GetItemCount());
            Assert.Equal("a", adapter.mCollection[0]);
            Assert.Equal("c", adapter.mCollection[1]);
        }

        [Fact]
        public void TestClear()
        {
            adapter.Clear();
            Assert.Equal(0, adapter.GetItemCount());
        }

        [Fact]
        public void TestSetPresenterAndDecorator()
        {
            var p = new Mock<BaseViewAdapter<string>.Presenter>().Object;
            adapter.SetPresenter(p);
            Assert.Equal(p, adapter.GetPresenter());

            var d = new Mock<BaseViewAdapter<string>.Decorator>().Object;
            adapter.SetDecorator(d);
            Assert.NotNull(adapter.mDecorator);
        }
    }
}