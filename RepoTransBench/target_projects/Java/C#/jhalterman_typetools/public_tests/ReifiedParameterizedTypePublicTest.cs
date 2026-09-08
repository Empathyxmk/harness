using System;
using System.Reflection;
using Xunit;

namespace TypeTools.Tests.Public
{
    public class ReifiedParameterizedTypePublicTest
    {
        private class PublicSample<X, Y> { }
        private static Type GetParameterizedType()
        {
            var f = typeof(PublicSampleHolder).GetField("sample", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static);
            return f.FieldType;
        }

        private class PublicSampleHolder
        {
            public PublicSample<double, char> sample;
        }

        [Fact]
        public void TestAddReifiedTypeArgument_Normal()
        {
            var pt = GetParameterizedType();
            var rpt = new TypeTools.ReifiedParameterizedType(pt);
            rpt.AddReifiedTypeArgument(typeof(double));
            rpt.AddReifiedTypeArgument(typeof(char));
            Assert.Equal(typeof(double), rpt.GetActualTypeArguments()[0]);
            Assert.Equal(typeof(char), rpt.GetActualTypeArguments()[1]);
        }

        [Fact]
        public void TestAddReifiedTypeArgument_Loop()
        {
            var pt = GetParameterizedType();
            var rpt = new TypeTools.ReifiedParameterizedType(pt);
            rpt.AddReifiedTypeArgument(rpt);
            rpt.AddReifiedTypeArgument(typeof(char));
            Assert.True(ReferenceEquals(rpt.GetActualTypeArguments()[0], rpt));
            Assert.Equal(typeof(char), rpt.GetActualTypeArguments()[1]);
            string str = rpt.ToString();
            Assert.Contains("...", str);
        }

        [Fact]
        public void TestAddReifiedTypeArgument_Overflow()
        {
            var pt = GetParameterizedType();
            var rpt = new TypeTools.ReifiedParameterizedType(pt);
            rpt.AddReifiedTypeArgument(typeof(double));
            rpt.AddReifiedTypeArgument(typeof(char));
            rpt.AddReifiedTypeArgument(typeof(float));
            Assert.Null(rpt.GetActualTypeArguments().Length > 2 ? rpt.GetActualTypeArguments()[2] : null);
        }

        [Fact]
        public void TestToString_OwnerType()
        {
            var paramType = GetParameterizedType();
            var rpt = new TypeTools.ReifiedParameterizedType(paramType);
            rpt.AddReifiedTypeArgument(null);
            rpt.AddReifiedTypeArgument(typeof(char));
            string s = rpt.ToString();
            Assert.Contains("null", s);
            Assert.Contains(typeof(char).FullName, s);
        }

        [Fact]
        public void TestEquals()
        {
            var pt = GetParameterizedType();
            var rpt1 = new TypeTools.ReifiedParameterizedType(pt);
            var rpt2 = new TypeTools.ReifiedParameterizedType(pt);
            rpt1.AddReifiedTypeArgument(typeof(double));
            rpt1.AddReifiedTypeArgument(typeof(char));
            rpt2.AddReifiedTypeArgument(typeof(double));
            rpt2.AddReifiedTypeArgument(typeof(char));
            Assert.True(rpt1.Equals(rpt2));
            Assert.True(rpt2.Equals(rpt1));

            var rpt3 = new TypeTools.ReifiedParameterizedType(pt);
            rpt3.AddReifiedTypeArgument(typeof(char));
            rpt3.AddReifiedTypeArgument(typeof(double));
            Assert.False(rpt1.Equals(rpt3));
        }

        [Fact]
        public void TestHashCode()
        {
            var pt = GetParameterizedType();
            var rpt1 = new TypeTools.ReifiedParameterizedType(pt);
            var rpt2 = new TypeTools.ReifiedParameterizedType(pt);
            rpt1.AddReifiedTypeArgument(typeof(double));
            rpt1.AddReifiedTypeArgument(typeof(char));
            rpt2.AddReifiedTypeArgument(typeof(double));
            rpt2.AddReifiedTypeArgument(typeof(char));
            Assert.Equal(rpt1.GetHashCode(), rpt2.GetHashCode());
        }

        [Fact]
        public void TestNotEquals_DifferentType()
        {
            var pt = GetParameterizedType();
            var rpt = new TypeTools.ReifiedParameterizedType(pt);
            Assert.False(rpt.Equals("public"));
            Assert.False(rpt.Equals(null));
        }
    }
}