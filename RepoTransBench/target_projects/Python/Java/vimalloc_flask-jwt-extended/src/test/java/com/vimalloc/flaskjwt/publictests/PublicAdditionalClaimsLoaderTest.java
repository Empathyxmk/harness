package com.vimalloc.flaskjwt.publictests;

import io.restassured.RestAssured;
import io.restassured.response.Response;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class PublicAdditionalClaimsLoaderTest {
    private static final String BASE_URI = "http://localhost:8080";

    @Test
    public void testAdditionalClaimsAreIncluded() {
        // Simulates test /protected endpoint returns {"role": "editor", "active": false}
        String jwtToken = "mocked_bbrown_jwt_token";
        Map<String, String> headers = new HashMap<>();
        headers.put("Authorization", "Bearer " + jwtToken);

        Response response = RestAssured.given()
                .baseUri(BASE_URI)
                .headers(headers)
                .when()
                .get("/protected")
                .then()
                .extract().response();
        assertEquals(200, response.statusCode());
        assertEquals("editor", response.jsonPath().getString("role"));
        assertFalse(response.jsonPath().getBoolean("active"));
    }
}