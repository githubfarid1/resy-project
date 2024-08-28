from pywifi import PyWiFi, const, Profile
import subprocess
def connect_to_wifi(ssid, password):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    
    # Remove all existing profiles
    iface.remove_all_network_profiles()
    
    # Create a new profile
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    
    # Add and connect to the new profile
    iface.add_network_profile(profile)
    iface.connect(profile)
    
    # Wait for connection
    import time
    time.sleep(10)
    
    # Check connection status
    if iface.status() == const.IFACE_CONNECTED:
        print(f"Successfully connected to {ssid}")
    else:
        print("Failed to connect")

# Replace 'yourSSID' and 'yourPassword' with your network's SSID and password
# 
# breakpoint()
if "DilarangMasuk" in str(subprocess.check_output(["netsh", "wlan", "show", "interfaces"])):
    connect_to_wifi('Redmi Note 9T', '358358358')
else:
    connect_to_wifi('DilarangMasuk', '358358358')        

