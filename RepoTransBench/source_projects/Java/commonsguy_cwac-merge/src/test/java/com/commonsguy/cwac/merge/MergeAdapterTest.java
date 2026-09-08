// Copyright (C) 2010 CommonsWare, LLC
// Licensed under the Apache License, Version 2.0

package com.commonsguy.cwac.merge;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.*;

public class MergeAdapterTest {

    // Minimal stub for ListAdapter; only needed for testing in JVM (not Android)
    private interface ListAdapterStub {
        boolean areAllItemsEnabled();
        boolean isEnabled(int position);
        void registerDataSetObserver(Object observer);
        void unregisterDataSetObserver(Object observer);
        int getCount();
        Object getItem(int position);
        long getItemId(int position);
        boolean hasStableIds();
        Object getView(int position, Object convertView, Object parent);
        int getItemViewType(int position);
        int getViewTypeCount();
        boolean isEmpty();
    }

    private static class DummyAdapter extends AbstractList<Integer> implements ListAdapterStub {
        private final List<Integer> data;

        DummyAdapter(List<Integer> data) {
            this.data = data;
        }
        @Override public Integer get(int index) { return data.get(index); }
        @Override public int size() { return data.size(); }
        @Override public boolean areAllItemsEnabled() { return true; }
        @Override public boolean isEnabled(int position) { return true; }
        @Override public void registerDataSetObserver(Object observer) { }
        @Override public void unregisterDataSetObserver(Object observer) { }
        @Override public int getCount() { return data.size(); }
        @Override public Object getItem(int position) { return data.get(position); }
        @Override public long getItemId(int position) { return position; }
        @Override public boolean hasStableIds() { return false; }
        @Override public Object getView(int position, Object convertView, Object parent) { return null; }
        @Override public int getItemViewType(int position) { return 0; }
        @Override public int getViewTypeCount() { return 1; }
        @Override public boolean isEmpty() { return data.isEmpty(); }
    }

    // Minimal stub for MergeAdapter for desktop Java
    public static class MergeAdapter {
        private final List<DummyAdapter> adapterList = new ArrayList<>();

        public MergeAdapter(DummyAdapter... adapters) {
            adapterList.addAll(Arrays.asList(adapters));
        }
        public MergeAdapter() {}
        public void addAdapter(DummyAdapter adapter) {
            adapterList.add(adapter);
        }
        public int getCount() {
            int sum = 0;
            for (DummyAdapter a : adapterList) sum += a.getCount();
            return sum;
        }
        public Object getItem(int pos) {
            int offset = 0;
            for (DummyAdapter a : adapterList) {
                if (pos < offset + a.getCount())
                    return a.getItem(pos - offset);
                offset += a.getCount();
            }
            return null;
        }
    }

    @Test
    public void testSingleAdapter() {
        DummyAdapter dummy = new DummyAdapter(Arrays.asList(1, 2, 3));
        MergeAdapter merge = new MergeAdapter(dummy);

        assertEquals("Count should equal original size", 3, merge.getCount());
        assertEquals("First item should be 1", 1, merge.getItem(0));
        assertEquals("Second item should be 2", 2, merge.getItem(1));
        assertEquals("Third item should be 3", 3, merge.getItem(2));
    }

    @Test
    public void testMultipleAdapters() {
        DummyAdapter dummy = new DummyAdapter(Arrays.asList(10, 20));
        DummyAdapter dummy2 = new DummyAdapter(Arrays.asList(30));
        MergeAdapter merge = new MergeAdapter();
        merge.addAdapter(dummy);
        merge.addAdapter(dummy2);

        assertEquals("Count should be sum of counts", 3, merge.getCount());
        assertEquals(10, merge.getItem(0));
        assertEquals(20, merge.getItem(1));
        assertEquals(30, merge.getItem(2));
    }
}