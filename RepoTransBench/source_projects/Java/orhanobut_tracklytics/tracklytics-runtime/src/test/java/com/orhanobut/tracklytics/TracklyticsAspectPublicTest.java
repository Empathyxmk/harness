package com.orhanobut.tracklytics;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.reflect.MethodSignature;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;

import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Map;

import static com.google.common.truth.Truth.assertThat;
import static org.mockito.Mockito.when;
import static org.mockito.MockitoAnnotations.initMocks;

@SuppressWarnings("ALL")
public class TracklyticsAspectPublicTest {

  @Mock ProceedingJoinPoint joinPoint;
  @Mock MethodSignature methodSignature;

  private final Map<String, Object> superAttributes = new HashMap<>();

  private TracklyticsAspect aspect;
  private TrackEvent trackEvent;
  private Map<String, Object> attributes;
  private AspectListener aspectListener;

  @Before public void setup() throws Exception {
    initMocks(this);

    aspectListener = new AspectListener() {
      @Override public void onAspectEventTriggered(TrackEvent trackEvent, Map<String, Object> attributes) {
        TracklyticsAspectPublicTest.this.trackEvent = trackEvent;
        TracklyticsAspectPublicTest.this.attributes = attributes;
      }

      @Override public void onAspectSuperAttributeAdded(String key, Object value) {
        superAttributes.put(key, value);
      }

      @Override public void onAspectSuperAttributeRemoved(String key) {
        superAttributes.remove(key);
      }
    };

    aspect = new TracklyticsAspect();
    aspect.subscribe(aspectListener);

    when(joinPoint.getSignature()).thenReturn(methodSignature);
  }

  private Method invokeMethod(Class<?> klass, String methodName, Class<?>... parameterTypes) throws Throwable {
    Method method = initMethod(klass, methodName, parameterTypes);
    Object instance = new Object();
    when(joinPoint.getThis()).thenReturn(instance);

    aspect.weaveJoinPointTrackEvent(joinPoint);
    return method;
  }

  private Method initMethod(Class<?> klass, String name, Class<?>... parameterTypes) throws Throwable {
    Method method = klass.getMethod(name, parameterTypes);
    when(methodSignature.getMethod()).thenReturn(method);
    return method;
  }

  @Test public void trackEventWithoutAttributesPublic() throws Throwable {
    class Bar {
      @TrackEvent("public_title") public void bar() {}
    }
    invokeMethod(Bar.class, "bar");

    assertTrack()
        .event("public_title")
        .noFilters()
        .noTags()
        .noAttributes();
  }

  @Test public void useReturnValueAsAttributePublic() throws Throwable {
    class Bar {
      @TrackEvent("public_event") @Attribute("pub_key") public String bar() { return "bar_data"; }
    }

    when(joinPoint.proceed()).thenReturn("bar_data");
    invokeMethod(Bar.class, "bar");

    assertTrack()
        .event("public_event")
        .noTags()
        .noFilters()
        .attribute("pub_key", "bar_data");
  }

  @Test public void useReturnValueAndParametersAsAttributesPublic() throws Throwable {
    class Bar {
      @TrackEvent("eventA") @Attribute("keyA") public String bar(@Attribute("keyB") String param) { return "dataA"; }
    }

    when(joinPoint.proceed()).thenReturn("dataA");
    when(joinPoint.getArgs()).thenReturn(new Object[]{"dataB"});
    invokeMethod(Bar.class, "bar", String.class);

    assertTrack()
        .event("eventA")
        .noFilters()
        .noTags()
        .attribute("keyA", "dataA")
        .attribute("keyB", "dataB");
  }

  @Test public void useDefaultValueWhenThereIsNoReturnValuePublic() throws Throwable {
    class Bar {
      @TrackEvent("pubEv")
      @Attribute(value = "k1", defaultValue = "dfVal") public void bar() {}
    }
    invokeMethod(Bar.class, "bar");

    assertTrack()
        .event("pubEv")
        .noFilters()
        .noTags()
        .attribute("k1", "dfVal");
  }

  @Test public void useDefaultValueWhenParameterValueIsNullPublic() throws Throwable {
    class Bar {
      @TrackEvent("ev2") public void bar(@Attribute(value = "kkk", defaultValue = "dvvv") String val) {}
    }

    when(joinPoint.getArgs()).thenReturn(new Object[]{null});
    invokeMethod(Bar.class, "bar", String.class);

    assertTrack()
        .event("ev2")
        .noFilters()
        .noTags()
        .attribute("kkk", "dvvv");
  }

  // Minimal assertion helper for demonstration
  private TrackSession assertTrack() {
    return new TrackSession();
  }

  // Dummy class, in actual test replace with real assertion handling objects.
  private class TrackSession {
    TrackSession event(String event) { assertThat(trackEvent.value()).isEqualTo(event); return this; }
    TrackSession noFilters()    { assertThat(trackEvent.filters()).isEmpty(); return this; }
    TrackSession noTags()       { assertThat(trackEvent.tags()).isEmpty(); return this; }
    TrackSession noAttributes() { assertThat(attributes == null || attributes.isEmpty()).isTrue(); return this; }
    TrackSession attribute(String key, Object value) {
      assertThat(attributes.get(key)).isEqualTo(value);
      return this;
    }
  }
}