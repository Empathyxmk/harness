using Xunit;
using System.IO;
using Hankkin.Library;

namespace Hankkin.TaoBaoDetailDemo.Original.Tests
{
    public class MyImageLoaderTests
    {
        [Fact]
        public void Test_GetInstanceSingleton()
        {
            var loader1 = MyImageLoader.GetInstance();
            var loader2 = MyImageLoader.GetInstance();
            Assert.True(ReferenceEquals(loader1, loader2));
        }

        [Fact]
        public void Test_DisplayImageSignatures()
        {
            var loader = MyImageLoader.GetInstance();

            // "context" is a dummy object for interface parity
            var context = new object();
            var imageView = new object();
            var progressBar = new object();

            loader.DisplayImage(context, "http://example.com/img.png", imageView);
            loader.DisplayImage(context, "http://example.com/img2.png", imageView, progressBar);
            loader.DisplayImage(context, new FileInfo("nofile"), imageView);
            loader.DisplayImage(context, new FileInfo("nofile"), imageView, 100, 100);
            loader.DisplayImage(context, "http://example.com/img3.png", imageView, 100, 100, progressBar);
            loader.DisplayImage(context, "http://example.com/img4.png", imageView, 120, 80);
            loader.DisplayImageFitCenter(context, "http://example.com/img5.png", imageView, 80, 90);
            loader.DisplayImageCen(context, "http://example.com/img6.png", imageView, 40, 20);

            // No assertions; these calls should not throw
        }
    }
}