package org.editorconfig;

import java.util.List;

/**
 * Utility methods for EditorConfig.
 */
public class Utils {

    public interface OutPair {
        String getKey();
        String getVal();
    }

    public static String configValueForKey(List<OutPair> outPairs, String key) {
        for (OutPair outPair : outPairs) {
            if (outPair.getKey().equals(key)) {
                return outPair.getVal();
            }
        }
        return "";
    }

    public static String invalidConfigMessage(String value, String key, String file) {
        return "\"" + value + "\" is not a valid value for key for file " + file;
    }

    public static String appliedConfigMessage(String value, String key, String file) {
        return "Applied \"" + value + "\" as key for file " + file;
    }
}