package com.socialwifi.routeros.original;

import com.socialwifi.routeros.base_api.BaseApi;
import com.socialwifi.routeros.resource.Resource;
import com.socialwifi.routeros.api_structure.ApiStructure;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class TestBaseApi {

    @Test
    void testGetResourceReturnsResourceObject() {
        ApiStructure apiStructure = new ApiStructure();
        apiStructure.addResource("/interface");
        BaseApi baseApi = new BaseApi(mock(com.socialwifi.routeros.api_communicator.ApiCommunicator.class), apiStructure);

        Resource resource = baseApi.getResource("/interface");
        assertNotNull(resource);
        assertEquals("/interface", resource.getPath());
    }

    @Test
    void testGetResourceThrowsIfNotExist() {
        ApiStructure apiStructure = new ApiStructure();
        BaseApi baseApi = new BaseApi(mock(com.socialwifi.routeros.api_communicator.ApiCommunicator.class), apiStructure);

        assertThrows(IllegalArgumentException.class, () -> baseApi.getResource("/notexists"));
    }
}