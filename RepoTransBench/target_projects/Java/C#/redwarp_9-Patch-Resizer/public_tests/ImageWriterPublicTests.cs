using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using Xunit;
using Redwarp.NinePatchResizer.worker;

namespace Redwarp.NinePatchResizer.PublicTests
{
    public class ImageWriterPublicTests : IDisposable
    {
        private Bitmap img;
        private FileInfo outputFile;
        private FileInfo inputFile;

        public ImageWriterPublicTests()
        {
            img = new Bitmap(15, 8, PixelFormat.Format24bppRgb);
            using (var g = Graphics.FromImage(img))
            {
                g.FillRectangle(Brushes.Black, 1, 1, 13, 6);
                g.DrawRectangle(Pens.Black, 0, 0, 14, 7);
            }
            outputFile = new FileInfo(Path.GetTempFileName() + ".png");
            inputFile = new FileInfo(Path.GetTempFileName() + ".png");
            img.Save(inputFile.FullName, ImageFormat.Png);
        }

        public void Dispose()
        {
            try { outputFile?.Delete(); } catch {}
            try { inputFile?.Delete(); } catch {}
            img.Dispose();
        }

        [Fact]
        public void TestWritePNG()
        {
            ImageWriter.Write(img, Output.PNG, outputFile);
            Assert.True(outputFile.Exists);
            using var loaded = (Bitmap)Image.FromFile(outputFile.FullName);
            Assert.NotNull(loaded);
            Assert.Equal(img.Width, loaded.Width);
            Assert.Equal(img.Height, loaded.Height);
        }

        [Fact]
        public void TestWriteJPG()
        {
            var jpgOutput = new FileInfo(Path.GetTempFileName() + ".jpg");
            try
            {
                ImageWriter.Write(img, Output.JPG, jpgOutput);
                Assert.True(jpgOutput.Exists);
                using var loaded = (Bitmap)Image.FromFile(jpgOutput.FullName);
                Assert.NotNull(loaded);
                Assert.Equal(img.Width, loaded.Width);
                Assert.Equal(img.Height, loaded.Height);
            }
            finally
            {
                try { jpgOutput.Delete(); } catch { }
            }
        }

        [Fact]
        public void TestCopy()
        {
            var copyFile = new FileInfo(Path.GetTempFileName() + ".png");
            try
            {
                ImageWriter.Copy(inputFile, copyFile);
                Assert.True(copyFile.Exists);
                using var loaded = (Bitmap)Image.FromFile(copyFile.FullName);
                Assert.NotNull(loaded);
            }
            finally
            {
                try { copyFile.Delete(); } catch {}
            }
        }

        [Fact]
        public void TestCopyNullInputs()
        {
            ImageWriter.Copy(null, null);
            // Should not throw
        }
    }
}