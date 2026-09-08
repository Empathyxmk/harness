package aegis1980.hotspot;

public class HotSpotManager {
    private boolean enabled;
    private String ssid;
    private String password;

    public HotSpotManager() {
        this.enabled = false;
        this.ssid = "defaultSSID";
        this.password = "password";
    }

    public boolean isEnabled() {
        return enabled;
    }

    public String getSsid() {
        return ssid;
    }

    public String getPassword() {
        return password;
    }

    public boolean enableHotspot(String ssid, String password) {
        if (ssid == null || ssid.isEmpty() || password == null || password.length() < 8) {
            return false;
        }
        this.ssid = ssid;
        this.password = password;
        this.enabled = true;
        return true;
    }

    public void disableHotspot() {
        this.enabled = false;
    }
}