package me.ele.amigo;

import android.content.Context;
import java.io.File;
import org.junit.Test;

import static org.junit.Assert.*;

public class AmigoPublicTest {

    @Test
    public void publicTestWorkWithoutCheckingSignature() {
        Context context = null;
        File patchFile = null;
        try {
            Amigo.workLater(context, patchFile); // use different variant
        } catch (Exception ignore) {}
    }

    @Test
    public void publicTestWork() {
        Context context = null;
        File patchFile = null;
        try {
            Amigo.workLaterWithoutCheckingSignature(context, patchFile, null); // different variant
        } catch (Exception ignore) {}
    }
}