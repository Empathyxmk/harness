package com.hannesdorfmann.fragmentargs.bundler;

import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import android.os.Bundle;
import android.os.Parcelable;

import static org.junit.Assert.*;

public class CastedArrayListArgsBundlerTest {

    static class DummyParcelable implements Parcelable {
        @Override public int describeContents() { return 0; }
        @Override public void writeToParcel(android.os.Parcel dest, int flags) {}
        public static final Creator<DummyParcelable> CREATOR = new Creator<DummyParcelable>() {
            public DummyParcelable createFromParcel(android.os.Parcel in) { return new DummyParcelable(); }
            public DummyParcelable[] newArray(int size) { return new DummyParcelable[size]; }
        };
    }

    static class FakeBundle extends Bundle {
        ArrayList<? extends Parcelable> arrayList;

        @Override
        public void putParcelableArrayList(String key, ArrayList<? extends Parcelable> value) {
            this.arrayList = value;
        }

        @Override
        public <T extends Parcelable> ArrayList<T> getParcelableArrayList(String key) {
            return (ArrayList<T>) arrayList;
        }
    }

    @Test(expected = ClassCastException.class)
    public void testPutThrowsIfNotArrayList() {
        CastedArrayListArgsBundler bundler = new CastedArrayListArgsBundler();
        List<DummyParcelable> list = Arrays.asList(new DummyParcelable(), new DummyParcelable());
        bundler.put("key", list, new FakeBundle());
    }

    @Test
    public void testPutAndGetWithArrayList() {
        CastedArrayListArgsBundler bundler = new CastedArrayListArgsBundler();
        ArrayList<DummyParcelable> arrList = new ArrayList<>();
        arrList.add(new DummyParcelable());
        arrList.add(new DummyParcelable());
        FakeBundle bundle = new FakeBundle();
        bundler.put("key", arrList, bundle);

        ArrayList<DummyParcelable> result = bundler.get("key", bundle);
        assertEquals(arrList, result);
    }
}