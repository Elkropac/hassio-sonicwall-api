# hassio-sonicwall-api
 * tested on TZ-300W with firmware 6.5.3.3-3n
 
 * configuration in hassio
 ```yaml
 device_tracker:
  - platform: sonicwall_api
    url: "https://ip.address:port/api/sonicos" #required
    username_ro: 'ro-user' #required
    password_ro: 'password' #required
    device_tracker_interfaces: ['X0', 'X2:V20', 'X2:V23', 'W0:V20'] #optional , defaults to ['X0'] , can also be ['all']
    verify_ssl: True #optional , defaults to False
```
 * configuration in SonicWALL
   * goto System>Administration
   * enable SonicOS API and basic authentication (for now)
   * goto Users>Local Users
   * create read only admin

Note: there can be only one admin logged to SonicWALL, so hassio will probably log you out, when it connects to check for mac table, only user "administrator" has higher priority
