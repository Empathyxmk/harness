using System;
using JoonasVali.NaturalMouseMotion.Api;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.TestUtils
{
    public class MockSystemCalls : SystemCalls
    {
        public bool MoveCalled { get; private set; }
        public override void MoveMouse(int x, int y)
        {
            MoveCalled = true;
        }
    }
}