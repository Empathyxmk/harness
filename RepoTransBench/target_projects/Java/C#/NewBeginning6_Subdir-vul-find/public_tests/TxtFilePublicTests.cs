using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.PublicTests
{
    public class TxtFilePublicTests
    {
        [Fact]
        public void TestTxtFileApi()
        {
            string fname = "txtfilepublictest.txt";
            string text = "foo\nbar\nbaz";
            var fileUtil = new TxtFile();

            bool foundWrite = false;
            bool foundRead = false;

            // Find suitable write method
            foreach (var m in typeof(TxtFile).GetMethods())
            {
                if (m.Name.ToLower().Contains("write"))
                {
                    var parameters = m.GetParameters();
                    if (parameters.Length == 3
                        && parameters[0].ParameterType == typeof(string)
                        && parameters[1].ParameterType == typeof(string)
                        && parameters[2].ParameterType == typeof(bool))
                    {
                        if (m.IsStatic)
                        {
                            m.Invoke(null, new object[] { fname, text, false });
                        }
                        else
                        {
                            m.Invoke(fileUtil, new object[] { fname, text, false });
                        }
                        foundWrite = true;
                        break;
                    }
                }
            }
            Assert.True(foundWrite, "No suitable write method found in TxtFile");

            List<string>? readResult = null;
            foreach (var m in typeof(TxtFile).GetMethods())
            {
                if (m.Name.ToLower().Contains("read"))
                {
                    var parameters = m.GetParameters();
                    if (parameters.Length == 1 && parameters[0].ParameterType == typeof(string))
                    {
                        object? result;
                        if (m.IsStatic)
                        {
                            result = m.Invoke(null, new object[] { fname });
                        }
                        else
                        {
                            result = m.Invoke(fileUtil, new object[] { fname });
                        }
                        if (result is List<string> l)
                        {
                            readResult = l;
                            foundRead = true;
                            break;
                        }
                    }
                }
            }
            Assert.True(foundRead, "No suitable read method found in TxtFile");
            Assert.NotNull(readResult);
            Assert.Equal(3, readResult!.Count);
            Assert.Equal("foo", readResult[0]);
            Assert.Equal("bar", readResult[1]);
            Assert.Equal("baz", readResult[2]);
            File.Delete(fname);
        }
    }
}