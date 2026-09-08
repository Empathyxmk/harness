using Moq;
using Xunit;
using System.Collections.Generic;

namespace UberUX.Tests.Public
{
    public class CarsPagerAdapterPublicTest
    {
        UberUX.CarsPagerAdapter adapter;

        public CarsPagerAdapterPublicTest()
        {
            adapter = new UberUX.CarsPagerAdapter(new List<int> { 2, 3, 2 });
        }

        [Fact]
        public void GetCount_ReturnsListSize_Public()
        {
            Assert.Equal(3, adapter.getCount());
        }

        [Fact]
        public void IsViewFromObject_ReturnsTrueIfSame_Public()
        {
            var view = new object();
            Assert.True(adapter.isViewFromObject(view, view));
        }

        [Fact]
        public void InstantiateAndDestroyItem_NoCrash_Public()
        {
            var container = new Mock<object>().Object;
            adapter.instantiateItem(container, 1);
            adapter.destroyItem(container, 2, new object());
        }
    }
}