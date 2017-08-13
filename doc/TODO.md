# To do

## Todo points

* Harry: Finish `ansible_playbook.yaml` stage 2: actions after reboot.

    * (How to send mail to the user? Answer: Just send "To: $USER", thanks to the hackspace config the machine will forward it to the user's registered email address.)
    * Do we need NFS? Yes,
        * Ask Jasper to verify: seems only admins or so are there currently? Or can *all* hackspace members log in with LDAP and automatically get a home folder that we see here?
    * Configuration of connection to machine, and spindle settings and storing these (in Ansible)
    * Confirm setup of local groups for access etc (all hackspace members can log onto the machine, but only allowed members have access rights) -> needs to be unix groups local to each machine, since LDAP groups are restricted by space, and separate memberships are needed for each machine anyway
        * How:
            * CNC admin
                * can add and remove users 
            * CNC users
        * Ask Jasper: ideas for solution by LDAP, or store in MySQL and resolve usernames to UIDs when running ansible and set those in the /etc/groups file?
    * Spindle measurement and recording
    * Logging the Spindle measurement and recording
        * via MySQL in a new VM. Ask Jasper how.
        * which machine they've logged in to; time when they log in; time when logging out; time spindle started; time spindle stopped
        * tool to see totals for the day
            * and fire off an email at 6:00 AM to the user with that info
        * each machine will have a separate rate

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
    
