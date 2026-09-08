using System.Collections.Generic;
using Xunit;
using Newtonsoft.Json;

namespace DawishGoogleArchitectureDemo.PublicTests.CoreModelUtil
{
    public class JsonUtilPublicTest
    {
        public class Animal
        {
            public string type { get; set; }
            public int age { get; set; }
            public Animal(string type, int age) { this.type = type; this.age = age; }
            public override bool Equals(object obj)
            {
                if (obj == null || GetType() != obj.GetType()) return false;
                Animal other = (Animal)obj;
                return age == other.age && type == other.type;
            }
            public override int GetHashCode() => (type, age).GetHashCode();
        }

        [Fact]
        public void Str2JsonBean_WithDifferentData()
        {
            string animalJson = "{\"type\":\"Dog\",\"age\":4}";
            Animal animal = JsonConvert.DeserializeObject<Animal>(animalJson);
            Assert.NotNull(animal);
            Assert.Equal("Dog", animal.type);
            Assert.Equal(4, animal.age);
        }

        [Fact]
        public void JsonBean2Str_WithDifferentData()
        {
            Animal animal = new Animal("Cat", 2);
            string json = JsonConvert.SerializeObject(animal);
            Assert.Contains("\"type\":\"Cat\"", json);
            Assert.Contains("\"age\":2", json);
        }

        [Fact]
        public void JsonList2Str_WithDifferentData()
        {
            var animalList = new List<Animal>
            {
                new Animal("Horse", 7),
                new Animal("Rabbit", 1)
            };
            string json = JsonConvert.SerializeObject(animalList);

            Assert.StartsWith("[", json);
            Assert.Contains("\"type\":\"Horse\"", json);
            Assert.Contains("\"type\":\"Rabbit\"", json);
            Assert.EndsWith("]", json);
        }
    }
}