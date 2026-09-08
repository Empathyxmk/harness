package com.dearbinge.openapi;

import com.dearbinge.service.InfrastructDeal;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import javax.servlet.http.*;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class ParkingSpotDataTransTest {
    private ParkingSpotDataTrans controller;
    private HttpServletRequest request;
    private HttpServletResponse response;
    private HttpSession session;
    private PrintWriter writer;
    private StringWriter outContent;

    @BeforeEach
    public void setUp() throws Exception {
        controller = new ParkingSpotDataTrans();
        request = mock(HttpServletRequest.class);
        response = mock(HttpServletResponse.class);
        session = mock(HttpSession.class);
        when(request.getSession()).thenReturn(session);
        outContent = new StringWriter();
        writer = new PrintWriter(outContent, true);
        when(response.getWriter()).thenReturn(writer);

        // Use reflection to inject required fields
        Map<String, InfrastructDeal> dealMap = new HashMap<>();
        java.lang.reflect.Field mapField = controller.getClass().getDeclaredField("posDataServiceMap");
        mapField.setAccessible(true);
        mapField.set(controller, dealMap);

        java.lang.reflect.Field secField = controller.getClass().getDeclaredField("securityService");
        secField.setAccessible(true);
        secField.set(controller, Mockito.mock(com.dearbinge.data.api.SecurityService.class));
    }

    @Test
    public void testGetSession_Normal() throws Exception {
        when(session.getId()).thenReturn("abcde12345");
        controller.getSession(request, response);
        verify(session).setAttribute("username", "chubin");
        writer.flush();
        assertTrue(outContent.toString().contains("node3"));
        assertTrue(outContent.toString().contains("sessionid:abcde12345"));
    }

    @Test
    public void testGetSession_IOException() throws Exception {
        when(response.getWriter()).thenThrow(new java.io.IOException("write error"));
        controller.getSession(request, response);
        // Should not throw
    }

    @Test
    public void testGetUserName_NoSession() throws Exception {
        when(request.getSession()).thenReturn(null);
        StringWriter sw = new StringWriter();
        PrintWriter pw = new PrintWriter(sw, true);
        when(response.getWriter()).thenReturn(pw);
        controller.getUserName(request, response);
        pw.flush();
        assertTrue(sw.toString().contains("no session found"));
    }

    @Test
    public void testGetUserName_NoAttribute() throws Exception {
        when(session.getAttribute("username")).thenReturn(null);
        controller.getUserName(request, response);
        writer.flush();
        assertTrue(outContent.toString().contains("no attribute found"));
    }

    @Test
    public void testGetUserName_WithUsername() throws Exception {
        when(session.getAttribute("username")).thenReturn("testuser");
        controller.getUserName(request, response);
        writer.flush();
        assertTrue(outContent.toString().contains("testuser"));
    }

    @Test
    public void testGetUserName_IOException() throws Exception {
        when(response.getWriter()).thenThrow(new java.io.IOException("fail"));
        assertThrows(java.io.IOException.class, () -> controller.getUserName(request, response));
    }

    @Test
    public void testCreate_noIdeal() throws Exception {
        when(request.getParameter("method")).thenReturn("notexist");
        controller.create(request, response);
        writer.flush();
        assertEquals("", outContent.toString());
    }

    @Test
    public void testCreate_withIdeal() throws Exception {
        String methodName = "sync";
        InfrastructDeal deal = mock(InfrastructDeal.class);
        when(deal.accept(request)).thenReturn("ok");
        java.lang.reflect.Field mapField = controller.getClass().getDeclaredField("posDataServiceMap");
        mapField.setAccessible(true);
        ((Map<String, InfrastructDeal>) mapField.get(controller)).put(methodName, deal);
        when(request.getParameter("method")).thenReturn(methodName);

        controller.create(request, response);
        verify(deal).accept(request);
        writer.flush();
        assertEquals("ok", outContent.toString());
    }

    @Test
    public void testCreate_IdealThrows() throws Exception {
        String methodName = "sync";
        InfrastructDeal deal = mock(InfrastructDeal.class);
        when(deal.accept(request)).thenThrow(new RuntimeException("fail"));
        java.lang.reflect.Field mapField = controller.getClass().getDeclaredField("posDataServiceMap");
        mapField.setAccessible(true);
        ((Map<String, InfrastructDeal>) mapField.get(controller)).put(methodName, deal);
        when(request.getParameter("method")).thenReturn(methodName);

        assertThrows(RuntimeException.class, () -> controller.create(request, response));
    }

    @Test
    public void testAddInterceptorsCoverage() {
        org.springframework.web.servlet.config.annotation.InterceptorRegistry registry = mock(org.springframework.web.servlet.config.annotation.InterceptorRegistry.class);
        when(registry.addInterceptor(any())).thenReturn(mock(org.springframework.web.servlet.config.annotation.InterceptorRegistration.class));
        controller.addInterceptors(registry);
        verify(registry, times(1)).addInterceptor(any());
    }
}