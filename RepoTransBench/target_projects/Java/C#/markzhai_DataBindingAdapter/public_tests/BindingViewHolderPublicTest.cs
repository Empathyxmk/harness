using Xunit;
using MarkZhai.DataBindingAdapter;

namespace MarkZhai.DataBindingAdapter.Tests.Public
{
    public class BindingViewHolderPublicTest
    {
        public class DummyBinding { }

        private DummyBinding binding;
        private object view;

        public BindingViewHolderPublicTest()
        {
            binding = new DummyBinding();
            view = new object();
        }

        [Fact]
        public void TestGetBindingPublic()
        {
            var holder = new BindingViewHolder<DummyBinding>(binding);
            Assert.Same(binding, holder.GetBinding());
        }
    }
}