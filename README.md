# lsm-control
Control software for a Zeiss LSM 21 / 31

## Hardware Notes
* Zeiss LSM
* USB GPIB Adapter
  * https://github.com/xyphro/UsbGpib
* Raspberry Pi

## Setup Notes
Install python modules:


```pip install pyvisa pyvisa-py pyusb```

Possibly also psutil zeroconf to avoid warnings when listing ressources.

Set up udev rules:

```
sudo nano /etc/udev/rules.d/99-usbtmc.rules
```
Add (maybe check vendor and product ID): 
```
SUBSYSTEMS=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2065", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usbmisc", KERNEL=="usbtmc0", MODE="0660", GROUP="plugdev"
```
Then run:
```
sudo udevadm control --reload-rules
sudo udevadm trigger
```
Replug LSM USB
