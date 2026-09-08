using System.Collections.Generic;
using Xunit;

namespace Vasco.Tests.Original
{
    public class ContextTransitionTableTest
    {
        private class DummyContext : Context<string, string, int>
        {
            private readonly int id;
            private readonly string methodName;

            public DummyContext(string method, int id)
                : base(method, default, false)
            {
                this.methodName = method;
                this.id = id;
            }
            public override int GetId() => id;
            public override string GetMethod() => methodName;
            public override bool Equals(object obj)
            {
                if (!(obj is DummyContext d)) return false;
                return id == d.id && methodName == d.methodName;
            }
            public override int GetHashCode() => id * 31 + methodName.GetHashCode();
        }

        private ContextTransitionTable<string, string, int> table;
        private DummyContext ctxA, ctxB;
        private CallSite<string, string, int> site1, site2;

        public ContextTransitionTableTest()
        {
            table = new ContextTransitionTable<string, string, int>();
            ctxA = new DummyContext("foo", 1);
            ctxB = new DummyContext("bar", 2);
            site1 = new CallSite<string, string, int>(ctxA, "node1");
            site2 = new CallSite<string, string, int>(ctxB, "node2");
        }

        [Fact]
        public void TestAddAndQueryTransitions()
        {
            Assert.False(table.HasCallers(ctxB));
            Assert.Null(table.GetCalledContexts(site1, "bar"));

            table.AddTransition(site1, ctxB);
            var called = table.GetCalledContexts(site1);
            Assert.Contains(ctxB, called);
            Assert.Equal(ctxB, table.GetCalledContexts(site1, "bar"));
            Assert.True(table.HasCallers(ctxB));

            table.AddTransition(site2, null);
            Assert.True(table.IsDefaultCallSite(site2));
            Assert.Contains(site2, table.GetDefaultCallSites());
        }

        [Fact]
        public void TestCallSitesOfContext()
        {
            table.AddCallSiteToContext(ctxA, site1);
            var s = table.GetCallSitesOfContext(ctxA);
            Assert.Contains(site1, s);
        }

        [Fact]
        public void TestGetCallers()
        {
            table.AddTransition(site1, ctxB);
            var callers = table.GetCallers(ctxB);
            Assert.Contains(site1, callers);
        }
    }
}