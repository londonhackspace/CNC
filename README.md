# CNC setup for London Hackspace

These are ansible scripts specific to the CNC machines. They are in a
separate repository so that they can be updated separately from the
general hackspace admins. 

This includes two stages: stage 1 installs LinuxCNC onto the machine
(fully automatically) while it (currently) runs off a net boot image,
then reboots it to load it. Stage 2 applies changes while LinuxCNC
running (and is useful for changes to previously installed machines,
too).

Stage 1 is mostly implemented as a Bash script in
[`scripts/stage1`](scripts/stage1) (an initial attempt to do all steps
in stage 1 in Ansible led to the conclusion that Ansible isn't well
suited for that, since dependency checking and continuation of the
install is relatively complex and such checks very convoluted to write
in Ansible). This step could (with slight adaptions) potentially be
used to install other machines with (variants of) Debian, too.

## How to use

1. turn on machine you want to be reinstalled
1. hit F12 key so that boot options come up, select 'network card'
1. select image "Wheezy AMD64 diskless" from list
    * note, this is to be changed to a special image for this purpuse. See "How to add a new netboot image" if not done.
1. `ssh root@boxfordcnc` (using ssh key, run once first to confirm ssh server key), or/then:
1. `ansible-playbook setup.yaml -i hosts`

setup.yaml runs both stage1.yaml and stage2.yaml.

So see what's going on in stage1, ssh root@<machine> then `cd stage1-logs; ls -lrt; less tmp.....`. This directory is currently persisted on the network image that's used, which may not persist or even be writable in the future. In case this happens, revert commit 184eeec28f771bec11b2c12a50f9b9dba7b9abe0.


## How to add a new netboot image

Someone with admin perms on `adminstuff` needs to do this (Christian):

    # debootstrap into /space/exports/export/images/$NEWDIR (?, or thereabouts)
    ssh you@adminstuff
    cd /tftpboot/pxelinux.cfg
    less default # look at "wheezy_amd64_diskless"
    # make directory /tftpboot/$NEWDIR
    # copy /tftpboot/amd64-wheezy/update.sh there, adapt, run it.
    vi default
    # add entry similar to "wheezy_amd64_diskless"
    
