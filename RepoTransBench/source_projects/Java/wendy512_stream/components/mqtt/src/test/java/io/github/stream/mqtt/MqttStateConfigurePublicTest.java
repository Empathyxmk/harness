// Public test for MqttStateConfigure (mirroring MqttStateConfigureTest but with different test data)
package io.github.stream.mqtt;

import io.github.stream.core.configuration.ConfigContext;
import org.junit.jupiter.api.Test;

import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class MqttStateConfigurePublicTest {

    @Test
    public void testSingletonInstancePublic() {
        MqttStateConfigure a = MqttStateConfigure.getInstance("uniqueOne");
        MqttStateConfigure b = MqttStateConfigure.getInstance("uniqueOne");
        assertSame(a, b);
        MqttStateConfigure c = MqttStateConfigure.getInstance("uniqueTwo");
        assertNotSame(a, c);
    }

    @Test
    public void testConfigureThrowsOnNullPublic() throws Exception {
        MqttStateConfigure instance = MqttStateConfigure.getInstance("cfgPublic");
        ConfigContext ctx = mock(ConfigContext.class, RETURNS_DEEP_STUBS);
        when(ctx.getInstance().getOriginal()).thenReturn(null);
        Exception ex = assertThrows(IllegalArgumentException.class, () -> {
            // reset flag
            instance.getClass().getDeclaredField("configured").setAccessible(true);
            ((java.util.concurrent.atomic.AtomicBoolean)instance.getClass().getDeclaredField("configured").get(instance)).set(false);
            instance.configure(ctx);
        });
        assertTrue(ex.getMessage().toLowerCase().contains("mqtt config cannot empty"));
    }

    @Test
    public void testConfigureSuccessIdempotentPublic() throws Exception {
        MqttStateConfigure instance = MqttStateConfigure.getInstance("anotherUnique");
        ConfigContext ctx = mock(ConfigContext.class, RETURNS_DEEP_STUBS);
        HashMap<String,Object> map = new HashMap<>();
        map.put("fooPublic", "barPublic");
        when(ctx.getInstance().getOriginal()).thenReturn(map);

        // static mock/stubbing of mqtt connection will go here if present, otherwise just call as is
        // reset flag
        instance.getClass().getDeclaredField("configured").setAccessible(true);
        ((java.util.concurrent.atomic.AtomicBoolean)instance.getClass().getDeclaredField("configured").get(instance)).set(false);

        // test should not throw for public test
        assertDoesNotThrow(() -> instance.configure(ctx));
        // idempotency: call again
        assertDoesNotThrow(() -> instance.configure(ctx));
    }
}