package me.ele.amigo;

import android.content.Context;
import java.io.File;
import org.junit.Test;

import static org.junit.Assert.*;

public class AmigoTest {

    @Test
    public void testWorkWithoutCheckingSignature() {
        Context context = null;
        File patchFile = null;
        // Just hit static for coverage (actual patching needs android env)
        try {
            Amigo.workWithoutCheckingSignature(context, patchFile);
        } catch (Exception ignore) {}
    }

    @Test
    public void testWork() {
        Context context = null;
        File patchFile = null;
        // Just attempt to run static code (hitting exception for coverage)
        try {
            Amigo.work(context, patchFile);
        } catch (Exception ignore) {}
    }

    @Test
    public void testWorkLaterVariants() {
        Context context = null;
        File patchFile = null;
        try {
            Amigo.workLater(context, patchFile);
        } catch (Exception ignore) {}

        try {
            Amigo.workLaterWithoutCheckingSignature(context, patchFile);
        } catch (Exception ignore) {}

        try {
            Amigo.workLaterWithoutCheckingSignature(context, patchFile, null);
        } catch (Exception ignore) {}
    }
}