using System.Collections.Generic;
using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.PublicTests
{
    public class HttpPublicTests
    {
        [Fact]
        public void TestResponseShape()
        {
            // Instead of a real call, use obviously invalid URL and test structure/shape of list
            string url = "http://example.invalid";
            string cookie = "mycookie=12345";
            string ua = "PublicAgent/2.0";
            string xHeaders = "X-Test: public\nTest-Header: 42";
            string method = "get";
            string dataBody = "";
            string enctypeBody = "application/json";
            bool follow = false;

            try
            {
                var response = Http.Response(url, cookie, ua, xHeaders, method, dataBody, enctypeBody, follow);
                Assert.NotNull(response);
                Assert.True(response.Count >= 4);
            }
            catch (System.Exception e)
            {
                Assert.True(false, "Http.Response() threw: " + e);
            }
        }
    }
}