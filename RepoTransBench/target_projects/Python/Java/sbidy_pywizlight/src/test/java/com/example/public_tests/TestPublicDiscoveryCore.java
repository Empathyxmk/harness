package com.example.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicDiscoveryCore {
    String wizMdnsName(String mac) {
        // Remove colons and capitalize
        String clean = mac.replace(":", "");
        return "WIZ_" + clean.toUpperCase() + "._wiz._udp.local.";
    }
    String defaultMac(String ip, int port) {
        // ip: "192.168.2.22" -> hex: C0A80216
        String[] parts = ip.split("\\.");
        StringBuilder sb = new StringBuilder();
        for (String p : parts)
            sb.append(String.format("%02X", Integer.valueOf(p)));
        sb.append(String.format("%04X", port));
        return sb.toString();
    }

    @Test
    public void testWizMdnsNamePublic() {
        String mac = "11:22:33:44:55:66";
        assertEquals("WIZ_112233445566._wiz._udp.local.", wizMdnsName(mac));
    }

    @Test
    public void testDefaultMacPublic() {
        String ip = "192.168.2.22";
        int port = 9020;
        String mac = defaultMac(ip, port);
        assertEquals("C0A80216232C", mac);
    }
}