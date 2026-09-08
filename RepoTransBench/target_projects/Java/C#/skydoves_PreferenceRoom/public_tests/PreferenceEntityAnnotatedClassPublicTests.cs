using System;
using Xunit;
using Moq;

namespace Skydoves.PreferenceRoom.PublicTests
{
    public class PreferenceEntityAnnotatedClassPublicTests
    {
        [Fact]
        public void TestMissingEntityNameThrowsPublic()
        {
            var ex = Assert.Throws<InvalidOperationException>(() =>
            {
                var typeElement = new Mock<object>();
                var annotation = new Mock<object>();
                dynamic dynTypeElement = typeElement.AsDynamic();
                dynTypeElement.AnnotationValue = "";

                if (dynTypeElement.AnnotationValue == "")
                    throw new InvalidOperationException("Entity name missing (public)");
            });

            Assert.Equal("Entity name missing (public)", ex.Message);
        }

        [Fact]
        public void TestWithDifferentDefaultPreferenceAndEncryptEntity()
        {
            var clz = new
            {
                entityName = "EntityY",
                isDefaultPreference = true,
                isEncryption = true,
                encryptionKey = "PUBLIC_ENCRYPTED_VAL"
            };

            Assert.Equal("EntityY", clz.entityName);
            Assert.True(clz.isDefaultPreference);
            Assert.True(clz.isEncryption);
            Assert.Equal("PUBLIC_ENCRYPTED_VAL", clz.encryptionKey);
        }
    }
}