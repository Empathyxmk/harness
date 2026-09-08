using Xunit;
using Moq;
using SlidingTabsBasic;
using SlidingTabsBasic.Common.View;
using System;

namespace OriginalTests
{
    public class SlidingTabsBasicFragmentTests
    {
        [Fact]
        public void TestOnCreateViewInflates()
        {
            var fragment = new SlidingTabsBasicFragment();
            var inflater = new Mock<dynamic>();
            var container = new Object();
            var bundle = new Object();
            var fakeView = new Object();

            inflater.Setup(i => i.Inflate(It.IsAny<int>(), container, false)).Returns(fakeView);

            var v = fragment.OnCreateView(inflater.Object, container, bundle);

            Assert.Equal(fakeView, v);
        }

        [Fact]
        public void TestOnViewCreated()
        {
            var fragment = new SlidingTabsBasicFragment();
            var view = new Mock<dynamic>();
            var pager = new Mock<dynamic>();
            var tabLayout = new Mock<dynamic>();

            view.Setup(v => v.FindViewById(It.IsAny<int>())).Returns((int id) =>
            {
                if (id == 0) return pager.Object;
                else return tabLayout.Object;
            });

            pager.Setup(p => p.SetAdapter(It.IsAny<SlidingTabsBasicFragment.SamplePagerAdapter>()));
            tabLayout.Setup(t => t.SetViewPager(pager.Object));

            fragment.OnViewCreated(view.Object, null);

            pager.Verify(p => p.SetAdapter(It.IsAny<SlidingTabsBasicFragment.SamplePagerAdapter>()), Times.AtLeastOnce());
            tabLayout.Verify(t => t.SetViewPager(pager.Object), Times.AtLeastOnce());
        }

        [Fact]
        public void TestSamplePagerAdapterGetCountIsTen()
        {
            var fragment = new SlidingTabsBasicFragment();
            var adapter = new SlidingTabsBasicFragment.SamplePagerAdapter();
            Assert.Equal(10, adapter.GetCount());
        }

        [Fact]
        public void TestIsViewFromObject()
        {
            var fragment = new SlidingTabsBasicFragment();
            var adapter = new SlidingTabsBasicFragment.SamplePagerAdapter();
            var v = new Object();

            Assert.True(adapter.IsViewFromObject(v, v));
            Assert.False(adapter.IsViewFromObject(new Object(), new Object()));
        }

        [Fact]
        public void TestGetPageTitle()
        {
            var fragment = new SlidingTabsBasicFragment();
            var adapter = new SlidingTabsBasicFragment.SamplePagerAdapter();

            for (int i = 0; i < adapter.GetCount(); i++)
            {
                Assert.Equal($"Item {i + 1}", adapter.GetPageTitle(i));
            }
        }
    }
}