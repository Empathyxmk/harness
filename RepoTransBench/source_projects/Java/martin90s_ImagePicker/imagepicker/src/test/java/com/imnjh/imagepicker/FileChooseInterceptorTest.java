package com.imnjh.imagepicker;

import android.content.Context;
import android.os.Parcel;
import android.os.Parcelable;

import org.junit.Test;
import java.util.ArrayList;

import static org.junit.Assert.*;

public class FileChooseInterceptorTest {
    static class DummyImpl implements FileChooseInterceptor {
        @Override
        public boolean onFileChosen(Context context, ArrayList<String> sel, boolean orig, int code, PickerAction action) {
            return sel != null && sel.size() > 0 && orig && code == 2 && action == null;
        }

        @Override
        public int describeContents() { return 0; }

        @Override
        public void writeToParcel(Parcel dest, int flags) { }

        public static final Parcelable.Creator<DummyImpl> CREATOR = new Parcelable.Creator<DummyImpl>() {
            @Override public DummyImpl createFromParcel(Parcel source) { return new DummyImpl(); }
            @Override public DummyImpl[] newArray(int size) { return new DummyImpl[size]; }
        };
    }

    @Test
    public void testOnFileChosen() {
        DummyImpl impl = new DummyImpl();
        ArrayList<String> sel = new ArrayList<>();
        sel.add("pic1");
        assertTrue(impl.onFileChosen(null, sel, true, 2, null));
    }

    @Test
    public void testParcelable() {
        DummyImpl impl = new DummyImpl();
        assertEquals(0, impl.describeContents());
        // Just test writeToParcel method for coverage
        impl.writeToParcel(null, 0);
        DummyImpl[] arr = DummyImpl.CREATOR.newArray(3);
        assertEquals(3, arr.length);
        DummyImpl inst = DummyImpl.CREATOR.createFromParcel(null);
        assertNotNull(inst);
    }
}