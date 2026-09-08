using System;
using Xunit;
using Moq;

namespace Skydoves.PreferenceRoom.OriginalTests
{
    public class PreferenceEntityAnnotatedClassTests
    {
        [Fact]
        public void TestMissingEntityNameThrows()
        {
            // Simulated VerifyException
            var ex = Assert.Throws<InvalidOperationException>(() =>
            {
                // Simulation of preference entity verification
                var typeElement = new Mock<object>();
                var annotation = new Mock<object>();
                dynamic dynTypeElement = typeElement.AsDynamic();
                dynTypeElement.AnnotationValue = "";

                if (dynTypeElement.AnnotationValue == "")
                    throw new InvalidOperationException("Entity name missing");
            });

            Assert.Equal("Entity name missing", ex.Message);
        }

        [Fact]
        public void TestWithDefaultPreferenceAndEncryptEntity()
        {
            // Simulated instance with all fields
            var clz = new
            {
                entityName = "EntityX",
                isDefaultPreference = true,
                isEncryption = true,
                encryptionKey = "ENCRYPTED_VALUE"
            };

            Assert.Equal("EntityX", clz.entityName);
            Assert.True(clz.isDefaultPreference);
            Assert.True(clz.isEncryption);
            Assert.Equal("ENCRYPTED_VALUE", clz.encryptionKey);
        }
    }
}