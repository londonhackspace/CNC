# To do

## Todo points

* Finish `ansible_playbook.yaml` stage 1: until reboot 

    * Do we also need NFS? Not sure which packages that requires. This might be set up by the main hackspace ansible scripts though, so just leave it for now.
    
    * Machine doesn't finish booting yet after running through stage1 for some reason. Investigate and fix.

    * wait_for still fails to work, bah 
     
* Finish `ansible_playbook.yaml` stage 2: actions after reboot. NOTE: perhaps it would be better to have different .yaml files for the two stages, so that they can be run separately manually. For a start, anyway. (How do you chain the two playbooks though (without merging them into one again) when wanting to have a one-action process in the future? You can always figure this out later though.)

    * add the the customisation of the Log on screen to ansibile 
        * https://wiki.debian.org/LightDM
    * Configuration of connection to machine, and spindle settings and storing these 
    * Spindle measurement and recording
    * Logging the Spindle measurement and recording
    * Confirm setup of local groups for access etc 

* what was the `bash` file in the repository for? Delete it?

* make copying the authorized_keys file also run after the machine is installed so that future changes to authorized_keys are synchronized (stage 2?). Be careful not to overwrite keys that have been added to the machine but not the ansible repository?

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


## Cosmetics

* Is there an ansible module to install packages? Doesn't really matter either way though since LinuxCNC is Debian only anyway.
