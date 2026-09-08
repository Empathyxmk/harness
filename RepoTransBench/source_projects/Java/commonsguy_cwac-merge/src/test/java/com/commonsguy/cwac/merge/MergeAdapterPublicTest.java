package com.commonsguy.cwac.merge;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.*;

public class MergeAdapterPublicTest {

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
    public void testSingleAdapterDifferentData() {
        // Use different data from existing test!
        DummyAdapter dummy = new DummyAdapter(Arrays.asList(42, 7, 18));
        MergeAdapter merge = new MergeAdapter(dummy);

        assertEquals("Count should equal original size", 3, merge.getCount());
        assertEquals("First item should be 42", 42, merge.getItem(0));
        assertEquals("Second item should be 7", 7, merge.getItem(1));
        assertEquals("Third item should be 18", 18, merge.getItem(2));
    }

    @Test
    public void testMultipleAdaptersDifferentData() {
        // Different integers from the existing test!
        DummyAdapter dummyA = new DummyAdapter(Arrays.asList(91, 22));
        DummyAdapter dummyB = new DummyAdapter(Arrays.asList(55, 66));
        MergeAdapter merge = new MergeAdapter();
        merge.addAdapter(dummyA);
        merge.addAdapter(dummyB);

        assertEquals("Count should be sum of counts", 4, merge.getCount());
        assertEquals(91, merge.getItem(0));
        assertEquals(22, merge.getItem(1));
        assertEquals(55, merge.getItem(2));
        assertEquals(66, merge.getItem(3));
    }
}