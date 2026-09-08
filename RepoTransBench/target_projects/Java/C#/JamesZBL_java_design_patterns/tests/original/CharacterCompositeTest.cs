using System;
using System.Text;
using Xunit;

namespace Tests.Original
{
    public class CharacterCompositeTest
    {
        [Fact]
        public void TestAddAndCount()
        {
            var composite = new TestCharacterComposite();
            Assert.Equal(0, composite.Count());
            composite.Add(new TestCharacterComposite());
            Assert.Equal(1, composite.Count());
        }

        [Fact]
        public void TestPrintNoChildren()
        {
            var composite = new TestCharacterComposite();
            // Should not throw
            composite.Print();
        }

        [Fact]
        public void TestPrintBeforeAfterHooks()
        {
            var composite = new HookTestCharacterComposite();
            composite.Print();
            Assert.True(composite.BeforeCalled);
            Assert.True(composite.AfterCalled);
        }

        [Fact]
        public void TestPrintDeepComposition()
        {
            var sb = new StringBuilder();
            var composite = new CustomPrintCharacterComposite(() => sb.Append("["), () => sb.Append("]"));
            var child = new CustomPrintCharacterComposite(() => sb.Append("A"), null);
            composite.Add(child);
            composite.Print();
            Assert.Equal("[A]", sb.ToString());
        }

        // Helper implementations for base abstract class as per pattern
        private class TestCharacterComposite : CharacterComposite
        {
        }
        private class HookTestCharacterComposite : CharacterComposite
        {
            public bool BeforeCalled = false, AfterCalled = false;
            public override void PrintBefore() { BeforeCalled = true; }
            public override void PrintAfter() { AfterCalled = true; }
        }
        private class CustomPrintCharacterComposite : CharacterComposite
        {
            private readonly Action _before, _after;
            public CustomPrintCharacterComposite(Action before, Action after) { _before = before; _after = after; }
            public override void PrintBefore() { _before?.Invoke(); }
            public override void PrintAfter() { _after?.Invoke(); }
        }
    }
}