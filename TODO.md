# To do

## Todo points

* Finish `ansible_playbook.yaml` part 1: until reboot (about done, except for dependency checking needs to be adapted to notice when machine is rebooted, suggestion: create a file on the /chroot/cnc/ somewhere and rely on that file being on the machine without the chroot/cnc prefix after reboot)
* Finish `ansible_playbook.yaml` part 2: actions after reboot
    * add the the customisation of the Log on screen to ansibile 
    * Configuration of connection to machine, and spindle settings and storing these 
    * Spindle measurement and recording
    * Logging the Spindle measurement and recording
    * Confirm setup of local groups for access etc 
    
## Spindle logging

Either/and:

* https://forum.linuxcnc.org/10-advanced-configuration/32388-recording-how-long-the-spindle-is-in-use
    * Christian:
    
        > I've had a quick look. The script is trivial except for the
        > hal stuff, so I looked this up, this page may be a good
        > starting point:
        > 
        > http://wiki.linuxcnc.org/cgi-bin/wiki.pl?HAL
        >
        > Anyway, just playing with it on the actual box will probably make things clear, perhaps it will work as is.

* disk image from gantry cnc on lattner:  unpack (where?), mount, see where the spindle logging stuff is (unless easier to do from the above)
