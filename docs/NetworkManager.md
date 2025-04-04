# NetworkManager

    I solved the problem. After upgrading Debian 11 to 12, OpenMediaVaulte created network configuration files in the \etc\netplan folder related to the interface, which in turn conflicted with the network manager and prevented it from starting its interfaces. I simply deleted the file from \etc\netplan and everything worked after rebooting.


## Check ip adress:

```bash
ip a

ip route
```

## Useful NetworkManager commands

```bash
nmcli general status
nmcli device status
nmcli connection show
```

## To **disable unattended-upgrades** in Debian, follow these steps:  

---

### ✅ **1. Disable the Service**  
Stop the service and prevent it from starting automatically:  
```bash
sudo systemctl stop unattended-upgrades.service
sudo systemctl disable unattended-upgrades.service
```

---

### ✅ **2. Remove or Comment the Auto-Upgrade Config**  
Edit the configuration file:  
```bash
sudo nano /etc/apt/apt.conf.d/20auto-upgrades
```
👉 Change or comment out these lines:  
```bash
// Disable automatic updates
APT::Periodic::Update-Package-Lists "0";
APT::Periodic::Unattended-Upgrade "0";
```

---

### ✅ **3. Remove the Package (Optional)**  
If you don’t need unattended-upgrades at all, uninstall it:  
```bash
sudo apt remove unattended-upgrades
```

---

### ✅ **4. Verify the Status**  
Check if the service is inactive:  
```bash
sudo systemctl status unattended-upgrades.service
```
👉 You should see `inactive (dead)` or `disabled`.  

---

### ✅ **5. Prevent Future Installation**  
If you want to ensure it doesn’t get installed again:  
```bash
sudo apt-mark hold unattended-upgrades
```

---

After these steps, **automatic updates should be completely disabled**. Let me know if you need anything else!

[HA Supervised - No Network Interfaces](https://community.home-assistant.io/t/ha-supervised-no-network-interfaces/681301)

### ✅ **Key Concepts of NetworkManager (nmcli):**  
1. **Check Device Status:**
   ```bash
   nmcli device status
   ```
   - Shows device states (connected, disconnected, unmanaged).  
   - If "unmanaged," NetworkManager isn't controlling the device.  

---

2. **Fixing Unmanaged State:**  
If `nmcli device status` shows `eth0` as unmanaged, it’s often due to:  
- A conflict with manual network settings.  
- NetworkManager not being configured to manage interfaces.  

To resolve it:  
1. Ensure NetworkManager controls the interface by editing `/etc/NetworkManager/NetworkManager.conf`:
   ```ini
   [keyfile]
   unmanaged-devices=none
   ```
2. Restart NetworkManager:  
   ```bash
   sudo systemctl restart NetworkManager
   ```

---

3. **Connecting Ethernet Manually:**  
To manually connect:  
```bash
nmcli device connect eth0
```
- Should establish a temporary connection until reboot.  

To make it persistent:  
```bash
nmcli connection modify eth0 connection.autoconnect yes
```
If multiple connections named "eth0" exist, use the UUID instead:  
```bash
nmcli connection modify <UUID> connection.autoconnect yes
```

---

4. **Removing Duplicate Connections:**  
If you have multiple connections named "eth0," delete extras using:  
```bash
nmcli connection delete <UUID>
```

---

5. **Verify Configuration:**  
Ensure the interface is up and connected after reboot:  
```bash
ip a
```
Look for `state UP` under `eth0` with an IP assigned.  

---

That should cover the main points. If you need more details or have follow-up questions, let me know!

Alright, let's troubleshoot deeper. It seems NetworkManager is still struggling to connect automatically. Let's verify the state of your connections and ensure a clean setup:  

---

### ✅ **Step 1: Cleanup Connections**
1. First, list all existing connections again:
   ```bash
   nmcli connection show
   ```

2. Delete all duplicate and unused connections **except** the Supervisor connection and main eth0 profile:
   ```bash
   sudo nmcli connection delete 3148b665-70a9-4bbc-b00e-7576225c23d0
   sudo nmcli connection delete 37f44767-dae4-4220-9b26-dbef8e22ea06
   sudo nmcli connection delete 19746725-8a9f-4305-b9e0-5cbf818bf3e3
   sudo nmcli connection delete 681b428f-beaf-8932-dce4-687ed5bae28e
   sudo nmcli connection delete fdb0812e-4e84-38d8-ad85-238888a77fdf
   ```

---

### ✅ **Step 2: Verify Connection Profiles**
1. Check the active Supervisor connection:  
   ```bash
   nmcli connection show 2b860928-2ceb-46e9-aa4d-1bf59a76b567
   ```
   Ensure it has the correct IP settings (likely DHCP).  

---

### ✅ **Step 3: Reset Eth0 Profile**  
1. Delete the main `eth0` profile:
   ```bash
   sudo nmcli connection delete b61d0ce2-abe4-4cfc-92a8-f7676e11d32d
   ```

2. Recreate it with auto-connect:
   ```bash
   sudo nmcli connection add type ethernet con-name eth0 ifname eth0
   sudo nmcli connection modify eth0 connection.autoconnect yes
   ```

---

### ✅ **Step 4: Check Link State**  
Ensure the Ethernet interface is up:  
```bash
sudo ip link set eth0 up
```

---

### ✅ **Step 5: Restart NetworkManager and Check**
1. Restart the service:
   ```bash
   sudo systemctl restart NetworkManager
   ```

2. Check network status:
   ```bash
   nmcli device status
   ```

---

### ✅ **Step 6: Test Supervisor Connectivity**
Verify Supervisor connection works:
```bash
nmcli connection up 2b860928-2ceb-46e9-aa4d-1bf59a76b567
```

---

### ✅ **Step 7: Reboot and Confirm**
Reboot your host:
```bash
sudo reboot
```

After reboot:
```bash
nmcli device status
ip a
```

---

Let me know the output after these steps!