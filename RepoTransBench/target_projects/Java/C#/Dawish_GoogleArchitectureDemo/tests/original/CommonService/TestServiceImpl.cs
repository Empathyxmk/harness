using System;

namespace DawishGoogleArchitectureDemo.Tests.Original.CommonService
{
    public class TestServiceImpl : ITestService
    {
        public string SayHello(string name)
        {
            // Simulated log output in C#
            Console.WriteLine($"TestServiceImpl sayHello : {name}");
            return "TestServiceImpl TestServiceImpl TestServiceImpl";
        }

        public void Init(object context)
        {
            Console.WriteLine("TestServiceImpl TestServiceImpl init");
        }
    }
}