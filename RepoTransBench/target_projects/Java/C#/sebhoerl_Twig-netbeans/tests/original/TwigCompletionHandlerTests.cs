using System;
using System.Collections.Generic;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.Tests.Original
{
    public class TwigCompletionHandlerTests
    {
        private readonly TwigCompletionHandler handler = new();

        [Fact]
        public void TestCompleteReturnsNone()
        {
            object ccc = null;
            var result = handler.Complete(ccc);
            Assert.Equal(TwigCompletionHandler.NONE, result);
        }

        [Fact]
        public void TestDocumentIsEmpty()
        {
            Assert.Equal("", handler.Document(null, null));
        }

        [Fact]
        public void TestResolveLinkIsNull()
        {
            Assert.Null(handler.ResolveLink("foo", null));
        }

        [Fact]
        public void TestGetPrefixIsEmpty()
        {
            Assert.Equal("", handler.GetPrefix(null, 0, true));
        }

        [Fact]
        public void TestAutoQuery()
        {
            object jtc = null;
            Assert.Equal(QueryType.ALL_COMPLETION, handler.GetAutoQuery(jtc, "foo"));
        }

        [Fact]
        public void TestResolveTemplateVariable()
        {
            Assert.Null(handler.ResolveTemplateVariable("foo", null, 1, "bar", new Dictionary<string, object>()));
        }

        [Fact]
        public void TestGetApplicableTemplates()
        {
            var result = handler.GetApplicableTemplates(null, 1, 2);
            Assert.Empty(result);
        }

        [Fact]
        public void TestParameters()
        {
            var pi = handler.Parameters(null, 1, null);
            Assert.NotNull(pi);
            Assert.Equal(0, pi.InsertIndex);
            Assert.Equal(0, pi.Offset);
            Assert.Empty(pi.ParametersList);
        }
    }
}