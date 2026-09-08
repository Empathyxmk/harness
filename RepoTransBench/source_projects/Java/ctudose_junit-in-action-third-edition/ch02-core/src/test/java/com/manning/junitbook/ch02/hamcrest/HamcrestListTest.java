package com.manning.junitbook.ch02.hamcrest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

public class HamcrestListTest {

    private List<String> customersNames;

    @BeforeEach
    public void setUp() {
        customersNames = new ArrayList<>();
        customersNames.add("John");
        customersNames.add("Michael");
        customersNames.add("Edwin");
    }

    @Test
    public void testListWithoutHamcrest() {
        org.junit.jupiter.api.Assertions.assertTrue(customersNames.contains("John") || customersNames.contains("Michael") || customersNames.contains("Edwin"));
    }

    @Test
    public void testListWithHamcrest() {
        // Corrected assertion to match the actual data setup in setUp()
        assertThat(customersNames, hasItems("John", "Michael", "Edwin"));
    }
}