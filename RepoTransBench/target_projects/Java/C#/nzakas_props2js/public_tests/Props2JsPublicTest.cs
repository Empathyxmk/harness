using System;
using Xunit;
using System.IO;
using System.Text;
using System.Collections.Generic;

namespace Props2Js.Tests.Public
{
    public class Props2JsPublicTest : IDisposable
    {
        // Need to restore streams after redirection
        private TextWriter _originalOut = Console.Out;
        private TextWriter _originalErr = Console.Error;

        private string CreateTempPropertiesFile(string content)
        {
            string path = Path.GetTempFileName();
            File.WriteAllText(path, content, Encoding.UTF8);
            return path;
        }

        [Fact]
        public void TestJsonStdout_public()
        {
            string props = "hello=world\ncount=128\nenabled=false";
            string file = CreateTempPropertiesFile(props);

            var sb = new StringBuilder();
            using (var writer = new StringWriter(sb))
            {
                Console.SetOut(writer);
                Props2Js.Main(new string[] { file });
                Console.Out.Flush();
            }
            Console.SetOut(_originalOut);

            string output = sb.ToString();
            Assert.Contains(@"""hello"":""world""", output);
            Assert.Contains(@"""count"":128", output);
            Assert.Contains(@"""enabled"":false", output);
        }

        [Fact]
        public void TestJsonOutputFile_public()
        {
            string props = "baz=qux";
            string file = CreateTempPropertiesFile(props);
            string outFile = Path.GetTempFileName();

            Props2Js.Main(new string[] { "-o", outFile, file });

            string content = File.ReadAllText(outFile, Encoding.UTF8);
            Assert.Contains(@"""baz"":""qux""", content);
        }

        [Fact]
        public void TestJsOutputTypeWithName_public()
        {
            string props = "alpha=omega\nnumval=12";
            string file = CreateTempPropertiesFile(props);
            string outFile = Path.GetTempFileName();

            Props2Js.Main(new string[] { "-o", outFile, "-t", "js", "-n", "newVar", file });

            string content = File.ReadAllText(outFile, Encoding.UTF8);
            Assert.True(content.StartsWith("var newVar=") || content.StartsWith("newVar="));
            Assert.Contains(@"""alpha"":""omega""", content);
        }

        [Fact]
        public void TestJsonpOutputTypeWithName_public()
        {
            string props = "b=22";
            string file = CreateTempPropertiesFile(props);
            string outFile = Path.GetTempFileName();

            Props2Js.Main(new string[] { "-o", outFile, "-t", "jsonp", "-n", "fCallback", file });

            string content = File.ReadAllText(outFile, Encoding.UTF8);
            Assert.StartsWith("fCallback(", content);
            Assert.EndsWith(");", content.Trim());
            Assert.Contains(@"""b"":22", content);
        }

        [Fact]
        public void TestHelpOption_public()
        {
            var sb = new StringBuilder();
            using (var writer = new StringWriter(sb))
            {
                Console.SetOut(writer);
                try
                {
                    Props2Js.Main(new string[] { "--help" });
                }
                catch
                {
                    // ignore
                }
                Console.Out.Flush();
            }
            Console.SetOut(_originalOut);
            var output = sb.ToString();
            Assert.Contains("props2js [options]", output);
        }

        [Fact]
        public void TestMissingInputFile_public()
        {
            Exception ex = Record.Exception(() => Props2Js.Main(new string[] { "--output", "nofile.js" }));
            Assert.NotNull(ex);
        }

        [Fact]
        public void TestMissingNameWithJsType_public()
        {
            string props = "some=99";
            string file = CreateTempPropertiesFile(props);

            Exception ex = Record.Exception(() => Props2Js.Main(new string[] { "-t", "js", file }));
            Assert.NotNull(ex);
        }

        [Fact]
        public void TestMissingNameWithJsonpType_public()
        {
            string props = "some=88";
            string file = CreateTempPropertiesFile(props);

            Exception ex = Record.Exception(() => Props2Js.Main(new string[] { "-t", "jsonp", file }));
            Assert.NotNull(ex);
        }

        [Fact]
        public void TestVerboseLogs_public()
        {
            string props = "welcome=here";
            string file = CreateTempPropertiesFile(props);

            var sb = new StringBuilder();
            using (var writer = new StringWriter(sb))
            {
                Console.SetError(writer);
                string outFile = Path.GetTempFileName();
                Props2Js.Main(new string[] { "-v", "-o", outFile, file });
                Console.Error.Flush();
            }
            Console.SetError(_originalErr);
            string logs = sb.ToString();
            Assert.Contains("Output file is", logs);
        }

        [Fact]
        public void TestDefaultOutputTypeIsJson_public()
        {
            string props = "foo=barz";
            string file = CreateTempPropertiesFile(props);

            var errSb = new StringBuilder();
            var outSb = new StringBuilder();
            using (var errWriter = new StringWriter(errSb))
            using (var outWriter = new StringWriter(outSb))
            {
                Console.SetError(errWriter);
                Console.SetOut(outWriter);
                Props2Js.Main(new string[] { "-v", file });
                Console.Error.Flush();
                Console.Out.Flush();
            }
            Console.SetError(_originalErr);
            Console.SetOut(_originalOut);
            string logs = errSb.ToString();
            Assert.Contains("defaulting to json", logs);
        }

        public void Dispose()
        {
            Console.SetOut(_originalOut);
            Console.SetError(_originalErr);
        }
    }
}