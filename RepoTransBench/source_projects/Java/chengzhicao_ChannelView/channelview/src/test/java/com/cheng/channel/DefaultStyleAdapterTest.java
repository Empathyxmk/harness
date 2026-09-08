package com.cheng.channel;

import android.content.Context;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.TextView;

import org.junit.Test;
import static org.junit.Assert.*;

public class DefaultStyleAdapterTest {
    static class TestAdapter extends DefaultStyleAdapter {
        public TestViewGroup parent;

        @Override
        public DefaultViewHolder createStyleView(ViewGroup parent, String channelName) {
            // For test, pass our own ViewGroup
            this.parent = (TestViewGroup) parent;
            return super.createStyleView(parent, channelName);
        }
    }

    static class TestViewGroup extends FrameLayout {
        public TestViewGroup(Context context) {
            super(context);
        }
    }

    @Test
    public void testCreateStyleView() {
        TestAdapter adapter = new TestAdapter();
        android.test.mock.MockContext mockContext = new android.test.mock.MockContext();
        TestViewGroup parent = new TestViewGroup(mockContext);
        DefaultStyleAdapter.DefaultViewHolder holder = adapter.createStyleView(parent, "MyChannel");
        assertTrue(holder.itemView instanceof TextView);
        assertEquals("MyChannel", ((TextView) holder.itemView).getText());
    }

    @Test
    public void testSetters() {
        TestAdapter adapter = new TestAdapter();
        android.test.mock.MockContext mockContext = new android.test.mock.MockContext();
        TextView view = new TextView(mockContext);
        // setTextColor
        adapter.setTextColor(view, 0xff112233);
        assertEquals(0xff112233, view.getCurrentTextColor());

        // setTextSize
        adapter.setTextSize(view, 18);
        assertEquals(18.0f, view.getTextSize(), 0.01);

        // setBackgroundResource (just invokes method, will not throw)
        adapter.setBackgroundResource(view, 0);
    }

    @Test
    public void testSetStyleMethods() {
        TestAdapter adapter = new TestAdapter();
        android.test.mock.MockContext mockContext = new android.test.mock.MockContext();
        TextView view = new TextView(mockContext);
        DefaultStyleAdapter.DefaultViewHolder holder = adapter.new DefaultViewHolder(view);

        adapter.setChannelNormalTextColor(0xf1);
        adapter.setChannelNormalBackground(0xa1);
        adapter.setChannelFixedTextColor(0xf2);
        adapter.setChannelFixedBackground(0xa2);
        adapter.setChannelEditBackground(0xa3);
        adapter.setChannelFocusedBackground(0xa4);
        adapter.setChannelFocusedTextColor(0xf3);

        // Should not throw
        adapter.setNormalStyle(holder);
        adapter.setFixedStyle(holder);
        adapter.setEditStyle(holder);
        adapter.setFocusedStyle(holder);
    }

    @Test
    public void testSetChannelTextSize() {
        TestAdapter adapter = new TestAdapter();
        adapter.setChannelTextSize(123);
    }
}