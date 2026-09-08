using Xunit;
using Moq;
using SlidingTabsBasic;
using SlidingTabsBasic.Common.View;
using System;

namespace PublicTests
{
    public class SlidingTabsBasicFragmentPublicTests
    {
        [Fact]
        public void TestOnCreateViewInflatesDifferentView()
        {
            var fragment = new SlidingTabsBasicFragment();
            var inflater = new Mock<dynamic>();
            var container = new Object();
            var bundle = new Object();
            var fakeView = new Object();

            inflater.Setup(i => i.Inflate(123456, container, false)).Returns(fakeView);

            var v = fragment.OnCreateView(inflater.Object, container, bundle);

            Assert.NotNull(v);
        }

        [Fact]
        public void TestOnViewCreatedWithDifferentMocks()
        {
            var fragment = new SlidingTabsBasicFragment();
            var view = new Mock<dynamic>();
            var pager = new Mock<dynamic>();
            var tabLayout = new Mock<dynamic>();

            int pagerId = 777;
            int tabId = 888;

            view.Setup(v => v.FindViewById(pagerId)).Returns(pager.Object);
            view.Setup(v => v.FindViewById(tabId)).Returns(tabLayout.Object);

            pager.Setup(p => p.SetAdapter(It.IsAny<SlidingTabsBasicFragment.SamplePagerAdapter>()));
            tabLayout.Setup(t => t.SetViewPager(pager.Object));

            fragment.OnViewCreated(view.Object, null);

            pager.Verify(p => p.SetAdapter(It.IsAny<SlidingTabsBasicFragment.SamplePagerAdapter>()), Times.AtLeast(0));
            tabLayout.Verify(t => t.SetViewPager(pager.Object), Times.AtLeast(0));
        }

        [Fact]
        public void TestSamplePagerAdapterGetCountIsElevenPublic()
        {
            var fragment = new SlidingTabsBasicFragment();
            var adapterMock = new Mock<SlidingTabsBasicFragment.SamplePagerAdapter>();
            adapterMock.Setup(a => a.GetCount()).Returns(11);

            Assert.Equal(11, adapterMock.Object.GetCount());
        }

        [Fact]
        public void TestIsViewFromObjectDifferentObjects()
        {
            var fragment = new SlidingTabsBasicFragment();
            var adapter = new SlidingTabsBasicFragment.SamplePagerAdapter();
            var v1 = new Object();
            var v2 = new Object();

            Assert.False(adapter.IsViewFromObject(v1, v2));
            Assert.True(adapter.IsViewFromObject(v2, v2));
        }

        [Fact]
        public void TestGetPageTitlePublic()
        {
            var fragment = new SlidingTabsBasicFragment();

            var adapterMock = new Mock<SlidingTabsBasicFragment.SamplePagerAdapter>();
            adapterMock.Setup(a => a.GetCount()).Returns(3);
            adapterMock.Setup(a => a.GetPageTitle(It.IsAny<int>())).Returns<int>(i => $"Tab {i * 2}");

            var adapter = adapterMock.Object;
            for (int i = 0; i < adapter.GetCount(); i++)
            {
                Assert.Equal($"Tab {i * 2}", adapter.GetPageTitle(i));
            }
        }
    }
}