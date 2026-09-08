package at.markushi.ui.action;

import android.os.Parcel;

import org.junit.Test;

import static org.junit.Assert.*;

public class LineSegmentTest {

    @Test
    public void testConstructorAndGetStartIdx() {
        LineSegment seg = new LineSegment(1, 2, 3);
        assertArrayEquals(new int[]{1, 2, 3}, seg.indexes);
        assertEquals(1, seg.getStartIdx());
    }

    @Test
    public void testParcelableWriteAndRead() {
        LineSegment seg = new LineSegment(4, 5, 6);
        Parcel parcel = Parcel.obtain();
        seg.writeToParcel(parcel, 0);
        parcel.setDataPosition(0);

        LineSegment created = LineSegment.CREATOR.createFromParcel(parcel);
        assertArrayEquals(new int[]{4, 5, 6}, created.indexes);

        LineSegment[] array = LineSegment.CREATOR.newArray(2);
        assertEquals(2, array.length);

        parcel.recycle();
    }

    @Test
    public void testDescribeContents() {
        LineSegment seg = new LineSegment(1, 2);
        assertEquals(0, seg.describeContents());
    }
}