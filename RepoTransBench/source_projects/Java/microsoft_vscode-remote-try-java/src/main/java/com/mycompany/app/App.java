package com.mycompany.app;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main(String[] args)
    {
        System.out.println(getMessage());
    }

    public static String getMessage() {
        return "Hello Remote World!";
    }

    // Added new code for testing branch and line coverage
    public static String evaluateNumber(int n) {
        if (n > 0) {
            if (n % 2 == 0) {
                return "Positive Even";
            } else {
                return "Positive Odd";
            }
        } else if (n < 0) {
            return "Negative";
        } else {
            return "Zero";
        }
    }
}