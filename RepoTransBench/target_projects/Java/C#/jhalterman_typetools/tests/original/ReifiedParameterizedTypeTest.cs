using System;
using System.Reflection;
using Xunit;

namespace TypeTools.Tests.Original
{
    public class ReifiedParameterizedTypeTest
    {
        private class Sample<A, B> { }

        private static Type GetParameterizedType()
        {
            var f = typeof(SampleHolder).GetField("sample", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static);
            return f.FieldType;
        }

        private class SampleHolder
        {
            public Sample<string, int> sample;
        }

        [Fact]
        public void TestAddReifiedTypeArgument_Normal()
        {
            var pt = GetParameterizedType();
            var rpt = new TypeTools.ReifiedParameterizedType(pt);
            rpt.AddReifiedTypeArgument(typeof(string));
            rpt.AddReifiedTypeArgument(typeof(int));
            Assert.Equal(typeof(string), rpt.GetActualTypeArguments()[0]);
            Assert.Equal(typeof(int), rpt.GetActualTypeArguments()[1]);
        }

        [Fact]
        public void TestAddReifiedTypeArgument_Loop()
        {
            var pt = GetParameterizedType();
            var rpt = new TypeTools.ReifiedParameterizedType(pt);
            rpt.AddReifiedTypeArgument(rpt); // self-loop
            rpt.AddReifiedTypeArgument(typeof(int));
            Assert.True(ReferenceEquals(rpt.GetActualTypeArguments()[0], rpt));
            Assert.Equal(typeof(int), rpt.GetActualTypeArguments()[1]);
            string str = rpt.ToString();
            Assert.Contains("...", str);
        }

        [Fact]
        public void TestAddReifiedTypeArgument_Overflow()
        {
            var pt = GetParameterizedType();
            var rpt = new TypeTools.ReifiedParameterizedType(pt);
            rpt.AddReifiedTypeArgument(typeof(string));
            rpt.AddReifiedTypeArgument(typeof(int));
            rpt.AddReifiedTypeArgument(typeof(bool)); // overflow
            Assert.Null(rpt.GetActualTypeArguments().Length > 2 ? rpt.GetActualTypeArguments()[2] : null);
        }

        [Fact]
        public void TestToString_OwnerType()
        {
            var paramType = GetParameterizedType();
            var rpt = new TypeTools.ReifiedParameterizedType(paramType);
            rpt.AddReifiedTypeArgument(null);
            rpt.AddReifiedTypeArgument(typeof(int));
            string s = rpt.ToString();
            Assert.Contains("null", s);
            Assert.Contains(typeof(int).FullName, s);
        }

        [Fact]
        public void TestEquals()
        {
            var pt = GetParameterizedType();
            var rpt1 = new TypeTools.ReifiedParameterizedType(pt);
            var rpt2 = new TypeTools.ReifiedParameterizedType(pt);
            rpt1.AddReifiedTypeArgument(typeof(string));
            rpt1.AddReifiedTypeArgument(typeof(int));
            rpt2.AddReifiedTypeArgument(typeof(string));
            rpt2.AddReifiedTypeArgument(typeof(int));
            Assert.True(rpt1.Equals(rpt2));
            Assert.True(rpt2.Equals(rpt1));

            var rpt3 = new TypeTools.ReifiedParameterizedType(pt);
            rpt3.AddReifiedTypeArgument(typeof(int));
            rpt3.AddReifiedTypeArgument(typeof(string));
            Assert.False(rpt1.Equals(rpt3));
        }

        [Fact]
        public void TestHashCode()
        {
            var pt = GetParameterizedType();
            var rpt1 = new TypeTools.ReifiedParameterizedType(pt);
            var rpt2 = new TypeTools.ReifiedParameterizedType(pt);
            rpt1.AddReifiedTypeArgument(typeof(string));
            rpt1.AddReifiedTypeArgument(typeof(int));
            rpt2.AddReifiedTypeArgument(typeof(string));
            rpt2.AddReifiedTypeArgument(typeof(int));
            Assert.Equal(rpt1.GetHashCode(), rpt2.GetHashCode());
        }

        [Fact]
        public void TestNotEquals_DifferentType()
        {
            var pt = GetParameterizedType();
            var rpt = new TypeTools.ReifiedParameterizedType(pt);
            Assert.False(rpt.Equals("x"));
            Assert.False(rpt.Equals(null));
        }
    }
}