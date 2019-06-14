# hassio-sonicwall-api
 * tested on TZ-300W with firmare 6.5.3.3-3n
 
 * configuration
 ```yaml
 device_tracker:
  - platform: sonicwall_api
    url: "https://ip.address:port/api/sonicos" #required
    username_ro: 'ro-user' #required
    password_ro: 'password' #required
    device_tracker_interfaces: ['X0', 'X2:V20', 'X2:V23', 'W0:V20'] #optional , defaults to ['X0'] , can also be ['all']
    verify_ssl: True #optional , defaults to False
```


    
 
