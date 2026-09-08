using System;
using Xunit;

namespace PayatuDivaAndroid.Tests.Original
{
    public class InputValidation2URISchemeActivity
    {
        public string WebViewUrl { get; set; } = "";
        public bool JavaScriptEnabled { get; set; } = true;
        public string InputUri { get; set; } = "";

        public void Get()
        {
            WebViewUrl = InputUri;
        }

        public void SetInputUri(string uri)
        {
            InputUri = uri;
        }
    }

    public class InputValidation2URISchemeActivityTests
    {
        private InputValidation2URISchemeActivity activity;

        public InputValidation2URISchemeActivityTests()
        {
            activity = new InputValidation2URISchemeActivity();
        }

        [Fact]
        public void Test_OnCreate_SetsLayoutAndJS()
        {
            Assert.True(activity.JavaScriptEnabled);
        }

        [Fact]
        public void Test_Get_LoadsUrlFromEditText()
        {
            activity.SetInputUri("https://payatu.com/");
            activity.Get();
            Assert.Equal("https://payatu.com/", activity.WebViewUrl);
        }
    }
}