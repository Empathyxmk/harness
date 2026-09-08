package com.dearbinge.service.impl;

import com.dearbinge.openapi.ParkingSpotDataTrans;
import com.dearbinge.service.impl.ParkingBasicDataSync;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import javax.servlet.http.HttpServletRequest;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class ParkingBasicDataSyncTest {

    private ParkingBasicDataSync dataSync;

    @BeforeEach
    void setup() {
        dataSync = new ParkingBasicDataSync();
    }

    @Test
    void testAcceptReturnsSuccess() {
        HttpServletRequest request = mock(HttpServletRequest.class);
        when(request.getParameter("jsonBody")).thenReturn("{\"key\":\"value\"}");
        String result = dataSync.accept(request);
        assertTrue(result.contains("success"));
    }

    @Test
    void testAcceptReturnsFail() {
        HttpServletRequest request = mock(HttpServletRequest.class);
        when(request.getParameter("jsonBody")).thenReturn(null);
        String result = dataSync.accept(request);
        assertTrue(result.contains("fail"));
    }

    @Test
    void testAcceptExceptionInParameter() {
        HttpServletRequest request = mock(HttpServletRequest.class);
        when(request.getParameter("jsonBody")).thenThrow(new RuntimeException("error"));
        String result = dataSync.accept(request);
        assertTrue(result.contains("fail"));
    }
}