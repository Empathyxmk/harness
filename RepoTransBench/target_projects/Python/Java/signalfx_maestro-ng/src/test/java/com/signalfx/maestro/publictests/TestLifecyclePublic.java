package com.signalfx.maestro.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class DummyService {
    public boolean enabled;
    public String state;
    public java.util.List<String> runActionCalls;

    public DummyService(boolean enabled) {
        this.enabled = enabled;
        this.state = "initialized";
        this.runActionCalls = new java.util.ArrayList<>();
    }

    public String runAction(String action) {
        runActionCalls.add(action);
        if (action.equals("activate")) {
            state = "activated";
        } else if (action.equals("deactivate")) {
            state = "deactivated";
        } else {
            state = "unknown_action";
        }
        return state;
    }
}

class DummyMaestroException extends RuntimeException {
    public DummyMaestroException(String m) { super(m); }
}

class PublicLifecycle {
    public static String runService(DummyService service, String action) {
        if (service.enabled == false) {
            return null;
        }
        try {
            return service.runAction(action);
        } catch (Exception e) {
            throw new DummyMaestroException(e.getMessage());
        }
    }
}

public class TestLifecyclePublic {

    @Test
    public void testRunEnabledServiceActivation() {
        DummyService service = new DummyService(true);
        PublicLifecycle.runService(service, "activate");
        assertEquals(java.util.Arrays.asList("activate"), service.runActionCalls);
        assertEquals("activated", service.state);
    }

    @Test
    public void testRunDisabledServiceNoAction() {
        DummyService service = new DummyService(false);
        PublicLifecycle.runService(service, "activate");
        assertEquals(java.util.Collections.emptyList(), service.runActionCalls);
        assertEquals("initialized", service.state);
    }

    @Test
    public void testRunServiceHandlesUnknownAction() {
        DummyService service = new DummyService(true);
        PublicLifecycle.runService(service, "suspend");
        assertEquals(java.util.Arrays.asList("suspend"), service.runActionCalls);
        assertEquals("unknown_action", service.state);
    }

    @Test
    public void testRunServiceExceptionHandling() {
        class FailingService extends DummyService {
            public FailingService(boolean enabled) { super(enabled); }
            @Override
            public String runAction(String action) {
                throw new DummyMaestroException("Simulated failure");
            }
        }
        DummyService service = new FailingService(true);
        assertThrows(DummyMaestroException.class, () -> PublicLifecycle.runService(service, "activate"));
    }
}