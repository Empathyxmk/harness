package com.doyensec.ajpfuzzer;

import java.util.*;

public class AJPTestCases {

    private static final List<String> tests;

    static {
        List<String> t = new ArrayList<>();
        t.add("GET /WEB-INF/web.xml");
        t.add("POST /admin HTTP/1.1");
        // Add more test cases as needed
        tests = Collections.unmodifiableList(t);
    }

    public static List<String> getAllCases() {
        return tests;
    }
}