using System;
using System.IO;
using Xunit;
using ArCpText;

namespace ArCpText.Tests.Original
{
    public class ImageUtilsTests : IDisposable
    {
        // Simulate temporary file setup/cleanup
        private string tempFile;

        [Fact]
        public void TestGetYUVByteSize()
        {
            Assert.Equal(4 * 4 + 2 * 2 * 2, ImageUtils.getYUVByteSize(4, 4));
            Assert.Equal(3 * 3 + 2 * 2 * 2, ImageUtils.getYUVByteSize(3, 3));
        }

        [Fact]
        public void TestConvertImageToBitmapCallsConvertYUV420ToARGB8888()
        {
            // Simulate: input and verify output shape (no actual image conversion)
            int[] output = new int[4];
            var result = ImageUtils.convertImageToBitmap(new object(), output, new byte[3][]);
            Assert.NotNull(result);
            Assert.Equal(4, result.Length);
        }

        [Fact]
        public void TestSaveBitmapToDiskCreatesFile()
        {
            // Create file and write bytes
            tempFile = Path.GetTempFileName();
            byte[] data = new byte[] { 1, 2, 3, 4 };
            ImageUtils.saveBitmapToDisk(data, tempFile);
            Assert.True(File.Exists(tempFile));
            Assert.Equal(4, new FileInfo(tempFile).Length);
        }

        [Fact]
        public void TestYUV2RGBClamping()
        {
            int rgb = ImageUtils.CallPrivateYUV2RGB(0, 255, 255);
            Assert.Equal(0xFF000000, rgb & unchecked((int)0xFF000000));
        }

        public void Dispose()
        {
            // Cleanup temp files if created
            if (!string.IsNullOrEmpty(tempFile) && File.Exists(tempFile))
            {
                File.Delete(tempFile);
            }
        }
    }
}