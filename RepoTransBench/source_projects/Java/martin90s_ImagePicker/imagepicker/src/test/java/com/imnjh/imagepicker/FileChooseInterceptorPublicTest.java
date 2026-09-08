package com.imnjh.imagepicker;

import android.content.Context;
import android.os.Parcel;
import android.os.Parcelable;

import org.junit.Test;
import java.util.ArrayList;

import static org.junit.Assert.*;

public class FileChooseInterceptorPublicTest {
    static class DummyImpl implements FileChooseInterceptor {
        @Override
        public boolean onFileChosen(Context context, ArrayList<String> sel, boolean orig, int code, PickerAction action) {
            // Slightly different than original test data
            return sel != null && sel.size() > 1 && !orig && code == 5 && action != null;
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
    public void testOnFileChosenWithDifferentData() {
        DummyImpl impl = new DummyImpl();
        ArrayList<String> sel = new ArrayList<>();
        sel.add("picA");
        sel.add("picB");
        // Provide different values: orig=false, code=5, action=not null
        assertTrue(impl.onFileChosen(null, sel, false, 5, new PickerAction(){}));
    }

    @Test
    public void testParcelableDifferentSize() {
        DummyImpl impl = new DummyImpl();
        assertEquals(0, impl.describeContents());
        // Write to Parcel (no-op)
        impl.writeToParcel(null, 0);
        DummyImpl[] arr = DummyImpl.CREATOR.newArray(2);
        assertEquals(2, arr.length);
        DummyImpl inst = DummyImpl.CREATOR.createFromParcel(null);
        assertNotNull(inst);
    }
}