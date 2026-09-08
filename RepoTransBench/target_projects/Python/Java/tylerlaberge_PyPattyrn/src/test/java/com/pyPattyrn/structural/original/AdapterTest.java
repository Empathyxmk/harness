package com.pyPattyrn.structural.original;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

import com.pyPattyrn.structural.adapter.Adapter;

class AdapterTest {

    interface Duck { String quack(); }
    static class Mallard { public String quackLoudly() { return "QUAAACK"; }}

    @Test
    void testAdapterWorks() {
        Mallard mallard = new Mallard();
        Adapter duckAdapter = new Adapter(mallard, new String[][]{{"quack", "quackLoudly"}});
        assertEquals("QUAAACK", duckAdapter.invoke("quack"));
    }
}