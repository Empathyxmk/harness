package at.markushi.ui.action;

import android.os.Parcel;

import org.junit.Test;

import static org.junit.Assert.*;

public class LineSegmentPublicTest {

    @Test
    public void testConstructorAndGetStartIdxPublic() {
        LineSegment seg = new LineSegment(10, 20, 30);
        assertArrayEquals(new int[]{10, 20, 30}, seg.indexes);
        assertEquals(10, seg.getStartIdx());
    }

    @Test
    public void testParcelableWriteAndReadPublic() {
        LineSegment seg = new LineSegment(7, 8, 9);
        Parcel parcel = Parcel.obtain();
        seg.writeToParcel(parcel, 0);
        parcel.setDataPosition(0);

        LineSegment created = LineSegment.CREATOR.createFromParcel(parcel);
        assertArrayEquals(new int[]{7, 8, 9}, created.indexes);

        LineSegment[] array = LineSegment.CREATOR.newArray(3);
        assertEquals(3, array.length);

        parcel.recycle();
    }

    @Test
    public void testDescribeContentsPublic() {
        LineSegment seg = new LineSegment(4, 8);
        assertEquals(0, seg.describeContents());
    }
}