using System;
using Xunit;
using System.IO;
using System.Text;
using System.Collections.Generic;

namespace Props2Js.Tests.Original
{
    public class Props2JsTest : IDisposable
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
        public void TestJsonStdout()
        {
            string props = "foo=bar\nnum=42\nflag=true";
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
            Assert.Contains(@"""foo"":""bar""", output);
            Assert.Contains(@"""num"":42", output);
            Assert.Contains(@"""flag"":true", output);
        }

        [Fact]
        public void TestJsonOutputFile()
        {
            string props = "foo=bar";
            string file = CreateTempPropertiesFile(props);
            string outFile = Path.GetTempFileName();

            Props2Js.Main(new string[] { "-o", outFile, file });

            string content = File.ReadAllText(outFile, Encoding.UTF8);
            Assert.Contains(@"""foo"":""bar""", content);
        }

        [Fact]
        public void TestJsOutputTypeWithName()
        {
            string props = "foo=bar\nval=5";
            string file = CreateTempPropertiesFile(props);
            string outFile = Path.GetTempFileName();

            Props2Js.Main(new string[] { "-o", outFile, "-t", "js", "-n", "resultVar", file });

            string content = File.ReadAllText(outFile, Encoding.UTF8);
            Assert.True(content.StartsWith("var resultVar=") || content.StartsWith("resultVar="));
            Assert.Contains(@"""foo"":""bar""", content);
        }

        [Fact]
        public void TestJsonpOutputTypeWithName()
        {
            string props = "a=1";
            string file = CreateTempPropertiesFile(props);
            string outFile = Path.GetTempFileName();

            Props2Js.Main(new string[] { "-o", outFile, "-t", "jsonp", "-n", "cb", file });

            string content = File.ReadAllText(outFile, Encoding.UTF8);
            Assert.StartsWith("cb(", content);
            Assert.EndsWith(");", content.Trim());
            Assert.Contains(@"""a"":1", content);
        }

        [Fact]
        public void TestHelpOption()
        {
            var sb = new StringBuilder();
            using (var writer = new StringWriter(sb))
            {
                Console.SetOut(writer);
                try
                {
                    Props2Js.Main(new string[] { "-h" });
                }
                catch
                {
                }
                Console.Out.Flush();
            }
            Console.SetOut(_originalOut);
            var output = sb.ToString();
            Assert.Contains("props2js [options]", output);
        }

        [Fact]
        public void TestMissingInputFile()
        {
            Exception ex = Record.Exception(() => Props2Js.Main(Array.Empty<string>()));
            Assert.NotNull(ex);
        }

        [Fact]
        public void TestMissingNameWithJsType()
        {
            string props = "x=1";
            string file = CreateTempPropertiesFile(props);

            Exception ex = Record.Exception(() => Props2Js.Main(new string[] { "-t", "js", file }));
            Assert.NotNull(ex);
        }

        [Fact]
        public void TestMissingNameWithJsonpType()
        {
            string props = "x=1";
            string file = CreateTempPropertiesFile(props);

            Exception ex = Record.Exception(() => Props2Js.Main(new string[] { "-t", "jsonp", file }));
            Assert.NotNull(ex);
        }

        [Fact]
        public void TestVerboseLogs()
        {
            string props = "foo=bar";
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
        public void TestDefaultOutputTypeIsJson()
        {
            string props = "y=world";
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