using System;
using Xunit;

namespace PayatuDivaAndroid.PublicTests
{
    public class InputValidation2URISchemeActivity
    {
        public string Input { get; private set; }

        public void SetInput(string val)
        {
            Input = val;
        }
    }

    public class InputValidation2URISchemeActivityPublicTests
    {
        [Fact]
        public void Test_UserInput_IsAccepted_Public()
        {
            var activity = new InputValidation2URISchemeActivity();
            string publicInput = "publicTestInput";
            activity.SetInput(publicInput);
            Assert.Equal(publicInput, activity.Input);
        }
    }
}