// Shim version for JVM testability
package edu.cmu.pocketsphinx;

public class Assets {
    private final String destDir;
    public Assets(Object context, String dest) {
        // ignore context for JVM test
        this.destDir = dest;
    }
    public Assets(Object context) {
        this(context, "default");
    }
    public void sync() throws Exception {
        throw new UnsupportedOperationException("No Android available in JVM");
    }
}