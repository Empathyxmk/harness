package org.caoym.jjvm;

import org.junit.Test;

import java.util.HashMap;

import static org.junit.Assert.*;

public class VirtualMachinePublicTest {

    @Test
    public void testSetAndGetUserVariableWithDifferentKey() {
        VirtualMachine vm = new VirtualMachine();
        String testKey = "public_key_2";
        Integer testVal = 7890;
        vm.setUserVariable(testKey, testVal);
        assertEquals(testVal, vm.getUserVariable(testKey));
    }

    @Test
    public void testSetAndGetMultipleUserVariables() {
        VirtualMachine vm = new VirtualMachine();
        vm.setUserVariable("user_var_one", 111);
        vm.setUserVariable("user_var_two", "hello");
        assertEquals(111, vm.getUserVariable("user_var_one"));
        assertEquals("hello", vm.getUserVariable("user_var_two"));
    }
}