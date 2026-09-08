using System;
using System.IO;

namespace NeonOrbit.Dexplore.Tests
{
    public static class TestUtilities
    {
        /// <summary>
        /// Gets a path to a sample DEX file for test purposes.
        /// </summary>
        public static string GetSampleDexFile()
        {
            // For demo: return a fixed test asset path.
            // In a real project, adapt to test asset management.
            var testAssetPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "sample.dex");
            if (!File.Exists(testAssetPath))
            {
                // Create a dummy sample.dex for demonstration
                File.WriteAllBytes(testAssetPath, new byte[] { 0x64, 0x65, 0x78, 0x0A }); // 'dex\n' header
            }
            return testAssetPath;
        }

        /// <summary>
        /// Loads a test DEX for testing search engine, etc.
        /// </summary>
        public static object LoadTestDex()
        {
            // Return a fake Dex object suitable for DexSearchEngine
            // You'll need to replace this with a proper object if available
            return new { Name = "com.example.MainActivity" };
        }
    }
}