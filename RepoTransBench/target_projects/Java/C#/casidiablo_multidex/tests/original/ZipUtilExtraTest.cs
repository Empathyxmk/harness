using System;
using System.IO;
using Xunit;

namespace Casidiablo.MultiDex.Tests.Original
{
    public class ZipUtilExtraTest
    {
        [Fact]
        public void TestFindCentralDirectoryShortFile()
        {
            var f = new FileInfo(Path.GetTempFileName() + ".zip");
            using (var fs = new FileStream(f.FullName, FileMode.Create))
            {
                fs.SetLength(1); // deliberately too short
            }
            Assert.Throws<System.IO.InvalidDataException>(() =>
            {
                using (var fs = new FileStream(f.FullName, FileMode.Open))
                {
                    ZipUtil.FindCentralDirectory(fs);
                }
            });
            f.Delete();
        }
    }
}