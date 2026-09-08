using System;
using Xunit;
using ArCpText;

namespace ArCpText.PublicTests
{
    public class TextRecognitionPublicTests
    {
        [Fact]
        public void TestDegreesToFirebaseRotationValidPublic()
        {
            var recog = new TextRecognition();
            Assert.Equal(0, recog.CallDegreesToFirebaseRotation(0));
            Assert.Equal(1, recog.CallDegreesToFirebaseRotation(90));
            Assert.Equal(2, recog.CallDegreesToFirebaseRotation(180));
            Assert.Equal(3, recog.CallDegreesToFirebaseRotation(270));
        }

        [Fact]
        public void TestDegreesToFirebaseRotationInvalidPublic()
        {
            var recog = new TextRecognition();
            Assert.Throws<ArgumentException>(() => recog.CallDegreesToFirebaseRotation(135));
        }
    }
}