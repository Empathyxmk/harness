package com.vimalloc.flaskjwt.publictests;

import org.junit.jupiter.api.Test;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;

public class PublicOptionsMethodTest {
    private static final String BASE_URI = "http://localhost:8080";
    @Test
    public void testOptionsAllowed() {
        // Simulate an OPTIONS request to "/endpoint"
        int statusCode = RestAssured.given()
                .contentType(ContentType.JSON)
                .when()
                .options(BASE_URI + "/endpoint")
                .getStatusCode();
        // Flask can return either 200 or 204 for OPTIONS.
        assert(statusCode == 200 || statusCode == 204);
    }
}