using System;

namespace WoodpeckerYsoserial.Tests.Annotation
{
    /// <summary>
    /// Attribute for parameterizing payload tests (analogous to @PayloadTest in Java).
    /// </summary>
    [AttributeUsage(AttributeTargets.Class, AllowMultiple = false, Inherited = true)]
    public class PayloadTestAttribute : Attribute
    {
        public string Skip { get; }
        public string Precondition { get; }
        public string Harness { get; }
        public string Flaky { get; }

        public PayloadTestAttribute(string skip = "", string precondition = "", string harness = "", string flaky = "")
        {
            Skip = skip;
            Precondition = precondition;
            Harness = harness;
            Flaky = flaky;
        }
    }
}