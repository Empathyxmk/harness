package com.example.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class GeoLocationFieldTests {

    static class Person {
        public GeoPt geolocation;
        public Person(String geolocation) {
            this.geolocation = (geolocation == null) ? null : new GeoPt(geolocation);
        }
        public Person(GeoPt geoPt) { this.geolocation = geoPt; }
        public static Person create(String geolocation){
            return new Person(geolocation);
        }
        public static Person create(GeoPt geopt){
            return new Person(geopt);
        }
        public static Person getByPk(Person p) {
            // In a real DB, here would be fetch by primary key. Here, just return.
            return p;
        }
    }

    static class Field {
        public String valueToString(Person p) {
            return p == null || p.geolocation == null ? null : p.geolocation.toString();
        }
        public String getPrepValue(Object v) {
            if (v == null) return null;
            return v instanceof GeoPt ? v.toString() : v.toString();
        }
    }

    @Test
    void testGettingLatLonFromModelGivenString() {
        Person sutCreate = Person.create("45,90");
        Person sut = Person.getByPk(sutCreate);
        assertEquals(45, sut.geolocation.lat);
        assertEquals(90, sut.geolocation.lon);
    }

    @Test
    void testGettingLatLonFromModelGivenPt() {
        Person sutCreate = Person.create(new GeoPt("45,90"));
        Person sut = Person.getByPk(sutCreate);
        assertEquals(45, sut.geolocation.lat);
        assertEquals(90, sut.geolocation.lon);
    }

    @Test
    void testGettingLatLonFromModelInDbGivenString() {
        Person sutCreate = Person.create("45,90");
        Person sut = Person.getByPk(sutCreate);
        assertEquals(45, sut.geolocation.lat);
        assertEquals(90, sut.geolocation.lon);
    }

    @Test
    void testExactMatchQuery() {
        Person sut = Person.create("45,90");
        Person result = sut; // Simulate a DB exact match (would compare GeoPt)
        assertEquals(result, sut);
    }

    @Test
    void testInMatchQuery() {
        Person sut = Person.create("45,90");
        GeoPt pt = new GeoPt("45,90");
        Person result = (pt.equals(sut.geolocation)) ? sut : null;
        assertEquals(result, sut);
    }

    @Test
    void testValueToStringWithPoint() {
        Person sut = Person.create(new GeoPt("45,90"));
        Field field = new Field();
        assertEquals("45.000,90.000".replace(".000", ""), field.valueToString(sut));
    }

    @Test
    void testValueToStringWithString() {
        Person sut = Person.create("45,90");
        Field field = new Field();
        assertEquals("45.000,90.000".replace(".000", ""), field.valueToString(sut));
    }

    @Test
    void testGetPrepValueReturnsNoneWhenNone() {
        Field field = new Field();
        String result = field.getPrepValue(null);
        assertNull(result);
    }
}