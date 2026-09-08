package com.doyensec.ajpfuzzer;

// Remove or comment out: import com.doyensec.ajp13.*;

import java.util.*;

public class Utils {

    private static final String DEFAULT_RANDOM_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789";

    public static String randomString(int length, String chars) {
        if (length < 0) throw new IllegalArgumentException("length must be >= 0");
        if (chars == null || chars.length() == 0) throw new IllegalArgumentException("chars must not be empty");
        StringBuilder sb = new StringBuilder();
        Random rand = new Random();
        for (int i = 0; i < length; ++i) {
            sb.append(chars.charAt(rand.nextInt(chars.length())));
        }
        return sb.toString();
    }

    public static int getRandomInt(int min, int max) {
        if (min > max) throw new IllegalArgumentException("min > max");
        if (min == max) return min;
        Random random = new Random();
        return random.nextInt((max - min) + 1) + min;
    }

    @SuppressWarnings("unchecked")
    public static <K, V> Map<K, V> createMapFromPairs(Object... args) {
        if (args.length % 2 != 0) {
            throw new IllegalArgumentException("Odd number of arguments");
        }
        Map<K, V> map = new HashMap<>();
        for (int i = 0; i < args.length; i += 2) {
            map.put((K) args[i], (V) args[i + 1]);
        }
        return map;
    }

    public static String toHex(byte[] b) {
        if (b == null) return null;
        StringBuilder sb = new StringBuilder();
        for (byte aB : b) {
            sb.append(String.format("%02x", aB & 0xff));
        }
        return sb.toString();
    }

    public static String join(String[] arr, String sep) {
        if (arr == null) return "";
        if (arr.length == 0) return "";
        StringBuilder sb = new StringBuilder(arr[0]);
        for (int i = 1; i < arr.length; ++i) {
            sb.append(sep).append(arr[i]);
        }
        return sb.toString();
    }
}