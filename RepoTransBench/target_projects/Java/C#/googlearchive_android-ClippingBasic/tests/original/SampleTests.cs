using System;
using Xunit;

// Dummy standins for Android classes
namespace ClippingBasicSample
{
    public class MainActivity
    {
        public object GetSupportFragmentManager() => new FragmentManager();
        public object FindViewById(int id)
        {
            return id switch
            {
                Resource.Id.Frame => new FrameView(),
                Resource.Id.TextView => new object(),
                Resource.Id.Button => new ButtonView(),
                _ => null
            };
        }
    }
    public class ClippingBasicFragment { }

    public class FragmentManager
    {
        public System.Collections.Generic.List<object> GetFragments()
        {
            // Create a stub list with dummy values to simulate index 1 being ClippingBasicFragment
            return new System.Collections.Generic.List<object>
            {
                new object(),
                new ClippingBasicFragment()
            };
        }
    }

    public static class Resource
    {
        public static class Id
        {
            public const int Frame = 1;
            public const int TextView = 2;
            public const int Button = 3;
        }
    }
    public class FrameView
    {
        private bool _clipToOutline = false;
        public bool GetClipToOutline() => _clipToOutline;
        public void SetClipToOutline(bool v) => _clipToOutline = v;
    }
    public class ButtonView { }
    public static class TouchUtils
    {
        public static void ClickView(object test, object btn)
        {
            if (btn is ButtonView && test is SampleTests)
            {
                // Simulate clicking sets the frame's ClipToOutline true
                var tests = (SampleTests)test;
                var frame = (FrameView)tests._mTestActivity.FindViewById(Resource.Id.Frame);
                frame.SetClipToOutline(true);
            }
        }
    }
}

namespace ClippingBasicSample.Tests.Original
{
    using ClippingBasicSample;

    public class SampleTests
    {
        internal MainActivity _mTestActivity;
        internal ClippingBasicFragment _mTestFragment;

        public SampleTests()
        {
            SetUp();
        }

        private void SetUp()
        {
            // Simulate activity launch and fragment setup
            _mTestActivity = new MainActivity();
            _mTestFragment = (ClippingBasicFragment)((FragmentManager)_mTestActivity.GetSupportFragmentManager()).GetFragments()[1];
        }

        [Fact]
        public void TestPreconditions()
        {
            Assert.NotNull(_mTestActivity);
            Assert.NotNull(_mTestFragment);
            Assert.NotNull(_mTestActivity.FindViewById(Resource.Id.Frame));
            Assert.NotNull(_mTestActivity.FindViewById(Resource.Id.TextView));
        }

        [Fact]
        public void TestClipping()
        {
            var clippedView = (FrameView)_mTestActivity.FindViewById(Resource.Id.Frame);
            Assert.False(clippedView.GetClipToOutline());
            TouchUtils.ClickView(this, _mTestActivity.FindViewById(Resource.Id.Button));
            Assert.True(clippedView.GetClipToOutline());
        }
    }
}