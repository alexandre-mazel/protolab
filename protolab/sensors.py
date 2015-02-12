import usb.core
import sys

# find our device
dev = usb.core.find(idVendor=0x0403, idProduct=0x6015)
print dev
print ("cfg:");
for cfg in dev:
    sys.stdout.write(str(cfg.bConfigurationValue) + '\n')
    for intf in cfg:
        sys.stdout.write('\t' + \
                         str(intf.bInterfaceNumber) + \
                         ',' + \
                         str(intf.bAlternateSetting) + \
                         '\n')
        for ep in intf:
            sys.stdout.write('\t\t' + \
                             str(ep.bEndpointAddress) + \
                             '\n')
print dev.read(1)