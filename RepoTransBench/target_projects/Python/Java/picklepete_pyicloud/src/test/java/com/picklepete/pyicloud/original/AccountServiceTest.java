package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.picklepete.pyicloud.services.PyiCloudServiceMock;
import com.picklepete.pyicloud.services.account.AccountService;
import com.picklepete.pyicloud.services.account.AccountDevice;
import com.picklepete.pyicloud.services.account.FamilyMember;
import com.picklepete.pyicloud.services.account.AccountStorage;
import com.picklepete.pyicloud.services.account.AccountStorageUsage;
import com.picklepete.pyicloud.services.account.AccountStorageUsageForMedia;

import java.util.Map;

public class AccountServiceTest {

    private AccountService service;

    @BeforeEach
    public void setUp() {
        PyiCloudServiceMock mock = new PyiCloudServiceMock(
                PyiCloudServiceMock.AUTHENTICATED_USER,
                PyiCloudServiceMock.VALID_PASSWORD
        );
        service = mock.getAccount();
    }

    @Test
    public void testRepr() {
        assertEquals("<AccountService: {devices: 2, family: 3, storage: 3020076244 bytes free}>", service.toString());
    }

    @Test
    public void testDevices() {
        assertNotNull(service.getDevices());
        assertEquals(2, service.getDevices().size());
        for (AccountDevice device : service.getDevices()) {
            assertNotNull(device.getName());
            assertNotNull(device.getModel());
            assertNotNull(device.getUdid());
            assertNotNull(device.get("serialNumber"));
            assertNotNull(device.get("osVersion"));
            assertNotNull(device.get("modelLargePhotoURL2x"));
            assertNotNull(device.get("modelLargePhotoURL1x"));
            assertNotNull(device.get("paymentMethods"));
            assertNotNull(device.get("name"));
            assertNotNull(device.get("model"));
            assertNotNull(device.get("udid"));
            assertNotNull(device.get("modelSmallPhotoURL2x"));
            assertNotNull(device.get("modelSmallPhotoURL1x"));
            assertNotNull(device.get("modelDisplayName"));
            String expected = "<AccountDevice: {model: " + device.getModelDisplayName() + ", name: " + device.getName() + "}>";
            assertEquals(expected, device.toString());
        }
    }

    @Test
    public void testFamily() {
        assertNotNull(service.getFamily());
        assertEquals(3, service.getFamily().size());
        for (FamilyMember member : service.getFamily()) {
            assertNotNull(member.getLastName());
            assertNotNull(member.getDsid());
            assertNotNull(member.getOriginalInvitationEmail());
            assertNotNull(member.getFullName());
            assertNotNull(member.getAgeClassification());
            assertNotNull(member.getAppleIdForPurchases());
            assertNotNull(member.getAppleId());
            assertNotNull(member.getFirstName());
            assertFalse(member.hasScreenTimeEnabled());
            assertFalse(member.hasAskToBuyEnabled());
            assertFalse(member.shareMyLocationEnabledFamilyMembers());
            assertNotNull(member.getDsidForPurchases());
            String expected = "<FamilyMember: {name: " + member.getFullName() +
                    ", age_classification: " + member.getAgeClassification() + "}>";
            assertEquals(expected, member.toString());
        }
    }

    @Test
    public void testStorage() {
        assertNotNull(service.getStorage());
        String actual = service.getStorage().toString();
        assertTrue(actual.contains("43.75% used of 5368709120 bytes"));
        assertTrue(actual.contains("photos"));
        assertTrue(actual.contains("backup"));
        assertTrue(actual.contains("docs"));
        assertTrue(actual.contains("mail"));
    }

    @Test
    public void testStorageUsage() {
        assertNotNull(service.getStorage().getUsage());
        AccountStorageUsage usage = service.getStorage().getUsage();
        assertTrue(usage.getCompStorageInBytes() >= 0 || usage.getCompStorageInBytes() == 0);
        assertTrue(usage.getUsedStorageInBytes() > 0);
        assertTrue(usage.getUsedStorageInPercent() > 0);
        assertNotNull(usage.getAvailableStorageInBytes());
        assertTrue(usage.getAvailableStorageInPercent() >= 0);
        assertTrue(usage.getTotalStorageInBytes() > 0);
        assertTrue(usage.getCommerceStorageInBytes() >= 0 || usage.getCommerceStorageInBytes() == 0);
        assertFalse(usage.getQuotaOver());
        assertFalse(usage.getQuotaTierMax());
        assertFalse(usage.getQuotaAlmostFull());
        assertFalse(usage.getQuotaPaid());
        String expectedStart = "<AccountStorageUsage: " + usage.getUsedStorageInPercent() +
                "% used of " + usage.getTotalStorageInBytes() + " bytes>";
        assertTrue(usage.toString().startsWith(expectedStart));
    }

    @Test
    public void testStorageUsagesByMedia() {
        Map<String, AccountStorageUsageForMedia> usagesByMedia = service.getStorage().getUsagesByMedia();
        assertNotNull(usagesByMedia);
        for (AccountStorageUsageForMedia usageMedia : usagesByMedia.values()) {
            assertNotNull(usageMedia.getKey());
            assertNotNull(usageMedia.getLabel());
            assertNotNull(usageMedia.getColor());
            assertTrue(usageMedia.getUsageInBytes() >= 0 || usageMedia.getUsageInBytes() == 0);
            String expected = "<AccountStorageUsageForMedia: {key: " + usageMedia.getKey() +
                    ", usage: " + usageMedia.getUsageInBytes() + " bytes}>";
            assertEquals(expected, usageMedia.toString());
        }
    }
}