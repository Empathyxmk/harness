using Xunit;
using Moq;
using MarkZhai.DataBindingAdapter;

namespace MarkZhai.DataBindingAdapter.Tests.Original
{
    public class BindingViewHolderTest
    {
        public class DummyBinding { }

        private DummyBinding binding;
        private object view;

        public BindingViewHolderTest()
        {
            binding = new DummyBinding();
            view = new object();
        }

        [Fact]
        public void TestGetBinding()
        {
            var holder = new BindingViewHolder<DummyBinding>(binding);
            Assert.Equal(binding, holder.GetBinding());
        }
    }
}