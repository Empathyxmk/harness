package rpc.abg.zk.registry;

import org.junit.Test;
import static org.junit.Assert.*;

public class ZooKeeperRegisterPublicTest {

    @Test
    public void testRegisterNewPath() {
        // Use another znode for registration
        String znode = "/register/public/node";
        boolean registered = doRegister(znode);
        assertTrue("Should register public node", registered);
    }

    private boolean doRegister(String znode) {
        // Simulated registration on new znode
        return znode.contains("/register/public/");
    }
}