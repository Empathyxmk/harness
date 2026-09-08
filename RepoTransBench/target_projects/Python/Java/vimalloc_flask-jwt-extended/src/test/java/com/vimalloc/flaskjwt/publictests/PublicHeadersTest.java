package com.vimalloc.flaskjwt.publictests;

import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import io.restassured.http.ContentType;
import io.restassured.response.Response;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class PublicHeadersTest {
    private static final String BASE_URI = "http://localhost:8080";

    @Test
    public void testCustomHeader() {
        String token = "mocked_token";
        Map<String, String> headers = new HashMap<>();
        headers.put("X-Custom-Auth", "Bearer " + token);

        Response response = RestAssured.given()
            .baseUri(BASE_URI)
            .headers(headers)
            .when()
            .get("/protected")
            .then()
            .extract().response();

        assertEquals(200, response.statusCode());
        assertEquals("header", response.jsonPath().getString("custom"));
    }

    @Test
    public void testInvalidHeaderType() {
        String token = "mocked_token";
        Map<String, String> headers = new HashMap<>();
        headers.put("X-Custom-Auth", "Token " + token);

        Response response = RestAssured.given()
            .baseUri(BASE_URI)
            .headers(headers)
            .when()
            .get("/protected")
            .then()
            .extract().response();

        assertEquals(401, response.statusCode());
        assertTrue(response.jsonPath().getString("msg").toLowerCase().startsWith("invalid"));
    }

    @Test
    public void testMissingCustomHeader() {
        Response response = RestAssured.given()
            .baseUri(BASE_URI)
            .when()
            .get("/protected")
            .then()
            .extract().response();

        assertEquals(401, response.statusCode());
        assertTrue(response.jsonPath().getString("msg").startsWith("Missing 'X-Custom-Auth' Header"));
    }
}