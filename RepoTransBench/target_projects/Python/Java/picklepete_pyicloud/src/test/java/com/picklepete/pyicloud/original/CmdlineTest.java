package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.picklepete.pyicloud.cmdline.CmdlineMain;
import com.picklepete.pyicloud.services.PyiCloudServiceMock;

import org.mockito.Mockito;
import org.mockito.MockedStatic;

import java.io.*;
import java.util.*;

public class CmdlineTest {

    CmdlineMain main;

    @BeforeEach
    public void setUp() {
        CmdlineMain.setServiceClass(PyiCloudServiceMock.class);
        main = new CmdlineMain();
    }

    @Test
    public void testNoArg() {
        assertThrows(SystemExitException.class, () -> main.run());
        assertThrows(SystemExitException.class, () -> main.run((String[])null));
        assertThrows(SystemExitException.class, () -> main.run(new String[]{}));
    }

    @Test
    public void testHelp() {
        assertThrows(SystemExitException.class, () -> main.run("--help"));
    }

    @Test
    public void testUsername() {
        assertThrows(SystemExitException.class, () -> main.run("--username"));
    }

    @Test
    public void testUsernamePasswordInvalid() {
        try (MockedStatic<CmdlineMain> mocked = Mockito.mockStatic(CmdlineMain.class, Mockito.CALLS_REAL_METHODS)) {
            mocked.when(() -> CmdlineMain.getPasswordFromKeyring(Mockito.anyString()))
                  .thenReturn(null);
            mocked.when(() -> CmdlineMain.getPass(Mockito.anyString()))
                  .thenReturn(null);

            assertThrows(SystemExitException.class, () -> main.run("--username", "invalid_user"));
            mocked.when(() -> CmdlineMain.getPass(Mockito.anyString()))
                  .thenReturn("invalid_pass");
            assertThrows(RuntimeException.class, () -> main.run("--username", "invalid_user"));
            assertThrows(RuntimeException.class,
                    () -> main.run("--username", "invalid_user", "--password", "invalid_pass"));
        }
    }

    @Test
    public void testUsernamePasswordRequires2FA() {
        try (MockedStatic<CmdlineMain> mocked = Mockito.mockStatic(CmdlineMain.class, Mockito.CALLS_REAL_METHODS)) {
            mocked.when(() -> CmdlineMain.getPasswordFromKeyring(Mockito.anyString()))
                  .thenReturn(null);
            mocked.when(() -> CmdlineMain.input(Mockito.anyString()))
                  .thenReturn(PyiCloudServiceMock.VALID_2FA_CODE);

            assertThrows(SystemExitException.class,
                    () -> main.run("--username", PyiCloudServiceMock.REQUIRES_2FA_USER,
                            "--password", PyiCloudServiceMock.VALID_PASSWORD,
                            "--non-interactive"));
        }
    }

    @Test
    public void testDeviceOutputfile() throws Exception {
        try (MockedStatic<CmdlineMain> mocked = Mockito.mockStatic(CmdlineMain.class, Mockito.CALLS_REAL_METHODS)) {
            mocked.when(() -> CmdlineMain.getPasswordFromKeyring(Mockito.anyString()))
                  .thenReturn(null);

            assertThrows(SystemExitException.class,
                    () -> main.run("--username", PyiCloudServiceMock.AUTHENTICATED_USER,
                            "--password", PyiCloudServiceMock.VALID_PASSWORD,
                            "--non-interactive", "--outputfile"));

            List<Map<String, Object>> devices = PyiCloudServiceMock.getFmiFamilyWorkingContent();
            for (Map<String, Object> device : devices) {
                String fname = device.get("name").toString().trim().toLowerCase() + ".fmip_snapshot";
                File pickleFile = new File(fname);
                assertTrue(pickleFile.exists());
                try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(pickleFile))) {
                    List<Object> contents = new ArrayList<>();
                    try {
                        Object obj;
                        while ((obj = ois.readObject()) != null) {
                            contents.add(obj);
                        }
                    } catch (EOFException e) {
                        // expected
                    }
                    assertEquals(List.of(device), contents);
                }
                pickleFile.delete();
            }
        }
    }
}