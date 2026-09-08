package rpc.abg.serialization.kryo;

import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.*;

class ByteBufOutputTest {

    @Test
    void testConstructorSetBuffer() {
        ByteBuf buf = Unpooled.buffer(8);
        ByteBufOutput out = new ByteBufOutput(buf);
        assertNotNull(out);
        out.setBuffer(null); // should not throw
    }

    @Test
    void testSetBufferWithCapacity() {
        ByteBuf buf = Unpooled.buffer(8);
        ByteBufOutput out = new ByteBufOutput(buf);
        out.setBuffer(buf, -1); // maxCapacity = safe max
        assertThrows(IllegalArgumentException.class, () ->
                out.setBuffer(buf, -2));
    }

    @Test
    void testWriteAndRelease() {
        ByteBuf buf = Unpooled.buffer(4);
        ByteBufOutput out = new ByteBufOutput(buf);

        out.write(65);
        assertEquals(1, buf.readableBytes());
        out.release();
        assertNull(out.byteBuf);
    }
}