package com.hannesdorfmann.fragmentargs.bundler;

import android.os.Bundle;
import android.os.Parcelable;
import android.os.Parcel;
import org.junit.Test;

import java.util.ArrayList;
import java.util.List;
import static org.junit.Assert.*;

/**
 * Public test for CastedArrayListArgsBundler using different test data.
 */
public class CastedArrayListArgsBundlerPublicTest {

    public static class MyParcelablePublic implements Parcelable {
        public String str;

        public MyParcelablePublic(String str) {
            this.str = str;
        }

        public MyParcelablePublic(Parcel in) {
            str = in.readString();
        }

        public static final Parcelable.Creator<MyParcelablePublic> CREATOR = new Parcelable.Creator<MyParcelablePublic>() {
            public MyParcelablePublic createFromParcel(Parcel in) {
                return new MyParcelablePublic(in);
            }
            public MyParcelablePublic[] newArray(int size) {
                return new MyParcelablePublic[size];
            }
        };

        @Override
        public int describeContents() { return 0; }

        @Override
        public void writeToParcel(Parcel dest, int flags) {
            dest.writeString(str);
        }

        @Override
        public boolean equals(Object o) {
            if (!(o instanceof MyParcelablePublic)) return false;
            return str.equals(((MyParcelablePublic) o).str);
        }

        @Override
        public int hashCode() {
            return str.hashCode();
        }
    }

    @Test
    public void testCastedArrayListArgsBundlerWithParcelable_publicVariant() {
        CastedArrayListArgsBundler bundler = new CastedArrayListArgsBundler();
        List<MyParcelablePublic> data = new ArrayList<>();
        data.add(new MyParcelablePublic("dragonfruit"));
        data.add(new MyParcelablePublic("peach"));
        data.add(new MyParcelablePublic("plum"));
        Bundle bundle = new Bundle();
        bundler.put("UniqueFruitKey", data, bundle);

        @SuppressWarnings("unchecked")
        List<MyParcelablePublic> restored = (List<MyParcelablePublic>) bundler.get("UniqueFruitKey", bundle);

        assertEquals(data, restored);
    }
}