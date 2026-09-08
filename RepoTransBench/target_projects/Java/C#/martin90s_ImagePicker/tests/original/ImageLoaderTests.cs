using System;
using Xunit;

namespace martin90s_ImagePicker.OriginalTests
{
    public interface IImageLoader
    {
        void BindImage(FakeImageView imageView, string uri, int width, int height);
        void BindImage(FakeImageView imageView, string uri);
        FakeImageView CreateImageView(object context);
        FakeImageView CreateFakeImageView(object context);
    }

    public class FakeImageView
    {
        public object? Tag;
        public FakeImageView(object context) { }
        public void SetTag(object tag) { Tag = tag; }
        public object? GetTag() => Tag;
    }

    public class ImageLoaderTests
    {
        private class DummyImageLoader : IImageLoader
        {
            public void BindImage(FakeImageView imageView, string uri, int width, int height)
            {
                if (imageView != null && uri != null)
                    imageView.SetTag(uri + width.ToString() + height.ToString());
            }
            public void BindImage(FakeImageView imageView, string uri)
            {
                if (imageView != null && uri != null)
                    imageView.SetTag(uri);
            }
            public FakeImageView CreateImageView(object context) => new FakeImageView(context);
            public FakeImageView CreateFakeImageView(object context) => new FakeImageView(context);
        }

        [Fact]
        public void TestImageLoaderBasic()
        {
            var loader = new DummyImageLoader();
            var ctx = new object();
            var image = new FakeImageView(ctx);
            string uri = "file://x.png";
            loader.BindImage(image, uri, 100, 200);
            Assert.IsType<string>(image.GetTag());
            loader.BindImage(image, uri);
            Assert.IsType<string>(image.GetTag());
            var iv1 = loader.CreateImageView(ctx);
            Assert.NotNull(iv1);
            var iv2 = loader.CreateFakeImageView(ctx);
            Assert.NotNull(iv2);
        }
    }
}