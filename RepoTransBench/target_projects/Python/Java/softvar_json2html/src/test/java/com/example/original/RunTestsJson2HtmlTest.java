package com.example.original;

import org.junit.platform.suite.api.IncludePackages;
import org.junit.platform.suite.api.SelectPackages;
import org.junit.platform.suite.api.Suite;

@Suite
// This suite includes all tests in package com.example.original
@SelectPackages("com.example.original")
@IncludePackages("com.example.original")
public class RunTestsJson2HtmlTest {
}