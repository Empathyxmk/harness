using Xunit;
using BlackObfuscatorASPlugin.Models;
using System.IO;

namespace BlackObfuscatorASPlugin.Tests.Original
{
    public class ObfDexTests
    {
        [Fact]
        public void TestObfNonExistentDir()
        {
            // Should not throw, input dir does not exist
            ObfDex.Obf("not/a/real/directory", 1, new string[0], new string[0], null);
        }

        [Fact]
        public void TestObfSingleFileThatIsNotDex()
        {
            string tmpFile = Path.GetTempFileName();
            try
            {
                ObfDex.Obf(Path.GetDirectoryName(tmpFile), 1, new string[0], new string[0], null);
            }
            finally
            {
                File.Delete(tmpFile);
            }
        }

        [Fact]
        public void TestObfEmptyDirectory()
        {
            string dir = Path.Combine(Path.GetTempPath(), $"empty_dir_for_obf_test_{System.DateTime.Now.Ticks}");
            Directory.CreateDirectory(dir);
            try
            {
                ObfDex.Obf(dir, 1, new string[0], new string[0], null);
            }
            finally
            {
                Directory.Delete(dir);
            }
        }
    }
}