using System;
using Xunit;
using CaoymJjvm;

namespace CaoymJjvm.PublicTests
{
    public class VirtualMachinePublicTest
    {
        [Fact]
        public void TestSetAndGetUserVariableWithDifferentKey()
        {
            var vm = new VirtualMachine();
            string testKey = "public_key_2";
            int testVal = 7890;
            vm.SetUserVariable(testKey, testVal);
            Assert.Equal(testVal, vm.GetUserVariable(testKey));
        }

        [Fact]
        public void TestSetAndGetMultipleUserVariables()
        {
            var vm = new VirtualMachine();
            vm.SetUserVariable("user_var_one", 111);
            vm.SetUserVariable("user_var_two", "hello");
            Assert.Equal(111, vm.GetUserVariable("user_var_one"));
            Assert.Equal("hello", vm.GetUserVariable("user_var_two"));
        }
    }
}