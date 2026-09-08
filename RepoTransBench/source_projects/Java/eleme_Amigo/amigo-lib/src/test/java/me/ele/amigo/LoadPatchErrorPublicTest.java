package me.ele.amigo;

import org.junit.Assert;
import org.junit.Test;

public class LoadPatchErrorPublicTest {

    @Test
    public void publicTestRecordDifferentType() {
        Exception err = new IllegalArgumentException("public exception");
        LoadPatchError recordedError = LoadPatchError.record(LoadPatchError.PATCH_ERR, err);
        Assert.assertEquals(err, recordedError.getException());
        Assert.assertEquals(LoadPatchError.PATCH_ERR, recordedError.getType());
    }
}