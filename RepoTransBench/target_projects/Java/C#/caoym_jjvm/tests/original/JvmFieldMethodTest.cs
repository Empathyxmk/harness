using System;
using Xunit;
using CaoymJjvm.Lang;
using CaoymJjvm.Runtime;

namespace CaoymJjvm.Tests.Original
{
    public class JvmFieldMethodTest
    {
        [Fact]
        public void TestJvmField()
        {
            var field = new TestJvmFieldImpl();
            field.Set(null, null, "abc");
            Assert.Equal("abc", field.Get(null, null));
        }

        class TestJvmFieldImpl : JvmField
        {
            private object _v;
            public override void Set(Env env, object thiz, object value) => _v = value;
            public override object Get(Env env, object thiz) => _v;
        }

        [Fact]
        public void TestJvmMethod()
        {
            var method = new TestJvmMethodImpl();
            method.Call(null, null, Array.Empty<object>());
            Assert.Equal(1, method.GetParameterCount());
            Assert.Equal("hello", method.GetName());
        }

        class TestJvmMethodImpl : IJvmMethod
        {
            public bool Called = false;
            public void Call(Env env, object thiz, params object[] args) { Called = true; }
            public int GetParameterCount() => 1;
            public string GetName() => "hello";
        }
    }
}