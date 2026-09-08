using Moq;
using Xunit;
using System.Collections.Generic;

namespace UberUX.Tests.Original
{
    public class CarsPagerAdapterTest
    {
        UberUX.CarsPagerAdapter adapter;

        public CarsPagerAdapterTest()
        {
            adapter = new UberUX.CarsPagerAdapter(new List<int> { 0, 1 });
        }

        [Fact]
        public void GetCount_ReturnsListSize()
        {
            Assert.Equal(2, adapter.getCount());
        }

        [Fact]
        public void IsViewFromObject_ReturnsTrueIfSame()
        {
            var view = new object();
            Assert.True(adapter.isViewFromObject(view, view));
        }

        [Fact]
        public void InstantiateAndDestroyItem_NoCrash()
        {
            var container = new Mock<object>().Object;
            adapter.instantiateItem(container, 0);
            adapter.destroyItem(container, 0, new object());
        }
    }
}