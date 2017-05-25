# To do

## Ask Jasper

* logins, admin, LDAP setup (just, get us to run ansible again)
* how to query email address?

## Todo points

* Finish `ansible_playbook.yaml` stage 1: until reboot 

    * [scripts/stage1](scripts/stage1) currently hard codes the host name (`boxfordcnc`):
        * How are we going to tell Ansible which host(s) to install? Probably via Ansible's `hosts:` thingie, pass this into the script call (argument, env var?)
    * It also hard codes the disk name (`/dev/sda`). Should this be a parameter, or should it ask for confirmation? By way of a wrapper script around calling Ansible?
    * `wait_for` for waiting after reboot still fails to work properly (...?, and how to handle change of ssh host key)

* Finish `ansible_playbook.yaml` stage 2: actions after reboot. NOTE: perhaps it would be better to have different .yaml files for the two stages, so that they can be run separately manually. For a start, anyway. (How do you chain the two playbooks though (without merging them into one again) when wanting to have a one-action process in the future? You can always figure this out later though.)

    * Do we need NFS?
    * running the general hackspace setup: document (needs a Hackspace Admin, and they will need documentation for how to run that step--probably including stage1 as new machines need their MAC address and hostname recorded (probably) before stage1 will work (which is still unfinished in this regard))
    * add the the customisation of the Log on screen to ansibile 
        * https://wiki.debian.org/LightDM
    * Configuration of connection to machine, and spindle settings and storing these 
    * Spindle measurement and recording
    * Logging the Spindle measurement and recording
    * Confirm setup of local groups for access etc 

* what was the `bash` file in the repository for? Delete it?

* make copying the authorized_keys file also run after the machine is installed so that future changes to authorized_keys are synchronized (stage 2?). Be careful not to overwrite keys that have been added to the machine but not the ansible repository? It's currently part of `stage1.yaml`.

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


## Add a new netboot image

Someone with admin perms on `adminstuff` should create a new netboot image just for our purpose, since we shouldn't hijack the other one (root pw / ssh keys, and log files from [scripts/stage1](scripts/stage1) written to `/root/...`):

    # debootstrap into /space/exports/export/images/$NEWDIR (?, or thereabouts)
    ssh you@adminstuff
    cd /tftpboot/pxelinux.cfg
    less default # look at "wheezy_amd64_diskless"
    # make directory /tftpboot/$NEWDIR
    # copy /tftpboot/amd64-wheezy/update.sh there, adapt, run it.
    vi default
    # add entry similar to "wheezy_amd64_diskless"
    
