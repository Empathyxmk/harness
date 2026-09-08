using System;
using System.Text;
using Xunit;

namespace PublicTests
{
    public class CharacterCompositePublicTest
    {
        [Fact]
        public void TestAddMultipleAndCountPublic()
        {
            var composite = new TestCharacterComposite();
            Assert.Equal(0, composite.Count());
            composite.Add(new TestCharacterComposite());
            composite.Add(new TestCharacterComposite());
            Assert.Equal(2, composite.Count());
        }

        [Fact]
        public void TestPrintNoChildrenPublic()
        {
            var composite = new TestCharacterComposite();
            composite.Print();
        }

        [Fact]
        public void TestPrintBeforeAfterHooksPublic()
        {
            var composite = new HookTestCharacterComposite();
            composite.Print();
            Assert.True(composite.BeforeCalled);
            Assert.True(composite.AfterCalled);
        }

        [Fact]
        public void TestPrintDeepCompositionPublic()
        {
            var sb = new StringBuilder();
            var composite = new CustomPrintCharacterComposite(() => sb.Append("<"), () => sb.Append(">"));
            var child = new CustomPrintCharacterComposite(() => sb.Append("B"), null);
            composite.Add(child);
            composite.Print();
            Assert.Equal("<B>", sb.ToString());
        }

        private class TestCharacterComposite : CharacterComposite { }
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