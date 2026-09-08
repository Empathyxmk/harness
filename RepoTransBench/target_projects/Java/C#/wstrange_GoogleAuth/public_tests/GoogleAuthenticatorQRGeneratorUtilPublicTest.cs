using System;
using System.Reflection;
using Xunit;

namespace GoogleAuth.PublicTests
{
    public class GoogleAuthenticatorQRGeneratorUtilPublicTest
    {
        [Fact]
        public void TestInternalURLEncodeNormal_public()
        {
            var method = typeof(GoogleAuthenticatorQRGenerator).GetMethod(
                "InternalURLEncode", BindingFlags.Static | BindingFlags.NonPublic);
            Assert.NotNull(method);
            var encoded = (string)method.Invoke(null, new object[] { "hello+world@example.org" });
            Assert.Contains("hello%2Bworld%40example.org", encoded);
        }

        [Fact]
        public void TestFormatLabelHappyPath_public()
        {
            var method = typeof(GoogleAuthenticatorQRGenerator).GetMethod(
                "FormatLabel", BindingFlags.Static | BindingFlags.NonPublic);
            Assert.NotNull(method);
            var label = (string)method.Invoke(null, new object[] { "OtherIssuer", "publicuser@domain.net" });
            Assert.Equal("OtherIssuer:publicuser@domain.net", label);

            label = (string)method.Invoke(null, new object[] { null, "bob" });
            Assert.Equal("bob", label);
        }

        [Fact]
        public void TestFormatLabelThrows_AccountNameNull_public()
        {
            var method = typeof(GoogleAuthenticatorQRGenerator).GetMethod(
                "FormatLabel", BindingFlags.Static | BindingFlags.NonPublic);
            Assert.NotNull(method);
            var ex = Assert.ThrowsAny<TargetInvocationException>(() =>
            {
                method.Invoke(null, new object[] { "Acme", null });
            });
            Assert.IsType<ArgumentException>(ex.InnerException);
        }

        [Fact]
        public void TestFormatLabelThrows_AccountNameEmpty_public()
        {
            var method = typeof(GoogleAuthenticatorQRGenerator).GetMethod(
                "FormatLabel", BindingFlags.Static | BindingFlags.NonPublic);
            Assert.NotNull(method);
            var ex = Assert.ThrowsAny<TargetInvocationException>(() =>
            {
                method.Invoke(null, new object[] { "Acme", "" });
            });
            Assert.IsType<ArgumentException>(ex.InnerException);
        }

        [Fact]
        public void TestFormatLabelThrows_IssuerContainsColon_public()
        {
            var method = typeof(GoogleAuthenticatorQRGenerator).GetMethod(
                "FormatLabel", BindingFlags.Static | BindingFlags.NonPublic);
            Assert.NotNull(method);
            var ex = Assert.ThrowsAny<TargetInvocationException>(() =>
            {
                method.Invoke(null, new object[] { "Not:Valid", "janedoe" });
            });
            Assert.IsType<ArgumentException>(ex.InnerException);
        }
    }
}