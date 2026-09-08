package org.ocpsoft.prettytime.jsf;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.ocpsoft.prettytime.PrettyTime;

import javax.faces.component.UIComponent;
import javax.faces.context.FacesContext;
import javax.faces.convert.ConverterException;
import java.util.Date;
import java.util.Locale;

import static org.junit.jupiter.api.Assertions.*;

class PrettyTimeConverterTest {

    static class DummyFacesContext extends FacesContext {
        private final DummyViewRoot viewRoot = new DummyViewRoot();
        @Override public DummyViewRoot getViewRoot() { return viewRoot; }
        // override other methods as needed with dummy implementations
    }

    static class DummyViewRoot extends javax.faces.component.UIViewRoot {
        private Locale locale = Locale.ENGLISH;
        @Override public Locale getLocale() { return locale; }
        @Override public void setLocale(Locale locale) { this.locale = locale; }
    }

    private PrettyTimeConverter converter;
    private FacesContext facesContext;
    private UIComponent uiComponent;

    @BeforeEach
    void setUp() {
        converter = new PrettyTimeConverter();
        facesContext = new DummyFacesContext();
        uiComponent = null; // not used in these tests
    }

    @Test
    void testGetAsStringWithValidDate() {
        ((DummyViewRoot)facesContext.getViewRoot()).setLocale(Locale.ENGLISH);
        Date now = new Date();
        String result = converter.getAsString(facesContext, uiComponent, now);
        assertNotNull(result);
        assertFalse(result.isEmpty());
    }

    @Test
    void testGetAsStringWithDifferentLocale() {
        ((DummyViewRoot)facesContext.getViewRoot()).setLocale(Locale.FRENCH);
        Date now = new Date();
        String result = converter.getAsString(facesContext, uiComponent, now);
        assertNotNull(result);
    }

    @Test
    void testGetAsStringThrowsForNull() {
        ConverterException ex = assertThrows(ConverterException.class, () ->
                converter.getAsString(facesContext, uiComponent, null)
        );
        assertTrue(ex.getMessage().contains("java.util.Date"));
    }

    @Test
    void testGetAsStringThrowsForNonDate() {
        ConverterException ex = assertThrows(ConverterException.class, () ->
                converter.getAsString(facesContext, uiComponent, "not a date")
        );
        assertTrue(ex.getMessage().contains("java.util.Date"));
        assertTrue(ex.getMessage().contains("String"));
    }

    @Test
    void testGetAsObjectThrowsAlways() {
        ConverterException ex = assertThrows(ConverterException.class, () ->
                converter.getAsObject(facesContext, uiComponent, "2020-01-01")
        );
        assertTrue(ex.getMessage().contains("Does not yet support"));
    }
}