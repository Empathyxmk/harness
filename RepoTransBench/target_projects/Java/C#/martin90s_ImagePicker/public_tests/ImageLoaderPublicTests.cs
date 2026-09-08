using Xunit;

namespace martin90s_ImagePicker.PublicTests
{
    public class FakeImageView
    {
        public object? Tag;
        public FakeImageView(object context) { }
        public void SetTag(object tag) { Tag = tag; }
        public object? GetTag() => Tag;
    }

    public interface IImageLoaderPublic
    {
        void Display(object context, string path, FakeImageView imageView, int width, int height);
        void Pause(object context);
        void Resume(object context);
        void ClearMemoryCache(object context);
        void ClearDiskCache(object context);
    }

    public class ImageLoaderPublicTests
    {
        private class DummyImageLoader : IImageLoaderPublic
        {
            public bool DisplayCalled = false;
            public bool PauseCalled = false;
            public bool ResumeCalled = false;
            public bool ClearMemCalled = false;
            public bool ClearDiskCalled = false;

            public void Display(object context, string path, FakeImageView imageView, int width, int height)
            {
                DisplayCalled = true;
            }
            public void Pause(object context)
            {
                PauseCalled = true;
            }
            public void Resume(object context)
            {
                ResumeCalled = true;
            }
            public void ClearMemoryCache(object context)
            {
                ClearMemCalled = true;
            }
            public void ClearDiskCache(object context)
            {
                ClearDiskCalled = true;
            }
        }

        [Fact]
        public void TestDisplayMethod_Public()
        {
            var loader = new DummyImageLoader();
            loader.Display(null, "some/path/public", null, 301, 401);
            Assert.True(loader.DisplayCalled);
        }

        [Fact]
        public void TestPauseAndResumeAndClearCaches_Public()
        {
            var loader = new DummyImageLoader();
            loader.Pause(null);
            Assert.True(loader.PauseCalled);
            loader.Resume(null);
            Assert.True(loader.ResumeCalled);
            loader.ClearMemoryCache(null);
            Assert.True(loader.ClearMemCalled);
            loader.ClearDiskCache(null);
            Assert.True(loader.ClearDiskCalled);
        }
    }
}