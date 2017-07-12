# CNC setup for London Hackspace

Purpose: setting up, and keeping up to date, machines running
[LinuxCNC](http://linuxcnc.org/) for the London Hackspace.

These are ansible scripts specific to the CNC machines. They are in a
separate repository so that they can be updated separately from the
general hackspace admins. 

This includes two stages: stage 1 installs LinuxCNC onto the machine
(fully automatically) while it (currently) runs off a net boot image,
then reboots it to load it. Stage 2 applies changes while LinuxCNC
running (and is useful for changes to previously installed machines,
too). Stage 2 really consists of two parts, Stage 2a which is the
general Hackspace setup, and Stage 2b which is the CNC specific
things.

Stage 1 is mostly implemented as a Bash script in
[`scripts/stage1`](scripts/stage1) (an initial attempt to do all steps
in stage 1 in Ansible led to the conclusion that Ansible isn't well
suited for that, since dependency checking and continuation of the
install is relatively complex and such checks very convoluted to write
in Ansible). This step could (with slight adaptions) potentially be
used to install other machines with (variants of) Debian, too.

## How to use

### Add a new machine

1. any CNC admin: figure out the MAC address of the machine to be (re)installed

1. a hackspace admin: 

    * log into boole `cd /etc/bind; less README` - git repo (if you don't understand the README, check through the git history for boxfordcnc via `git log -p`; run the signer command via sudo; then `sudo git commit -a -m "blabla"` (no push))
    * add IP and hostname for that MAC address: `cd /etc/dhcp; vim dhcpd.conf` - git repo
    * add the machine to the set of hosts to receive general Hackspace modifications
    * log into adminstuff
    
        * `sudo su` (or similar, keeping ssh key forwarding intact)
        * `ssh $HOSTNAME`, confirm ssh fingerprint 
        
            * If you get fingerprint *change* warnings, see the section "Updating sshfp records" in 
              [londonhackspace/ansible/README](https://github.com/londonhackspace/ansible/) (note: this page is only accessible if you're logged into Github and are a hackspace admin)
            
        * `cd /etc/ansible; ansible-playbook -D -l "cnc" lhs/site.yml`

1. any CNC admin: 

    1. turn on / reset the machine you want to be (re)installed. Hit key so that boot options come up (F12 for the machine used for 'boxfordcnc');

    1. boot:
    
        a. network boot, automatic network install via Debian debootstrap: currently **not working** because the parallel port is not being detected. Also, the new version of LinuxCNC may not be available quickly enough as Debian repository.

            1. select 'network card' (this works for the "Optiplex 760" (boxfordcnc), will be different for other machines). Select image "Wheezy i386 diskless" from list (*NOTE*, this is to be changed to a special image for this purpuse. See "Add a new netboot image" in [TODO](doc/TODO.md) if not done.)

                1. `ssh root@<hostname>` (`<hostname` being e.g. `boxfordcnc`, using ssh key, run once first to confirm that you can log in, and to add the ssh server key)
                1. run `make stage1` (or `make`) (TODO: how to specify host in question?)

                    * So see what's going on in stage1, `ssh root@<hostname>` then `cd stage1-logs; ls -lrt; less tmp.....`. This directory is currently persisted on the network image that's used, which may not persist or even be writable in the future. In case this happens, revert commit 184eeec28f771bec11b2c12a50f9b9dba7b9abe0.

        b. LinuxCNC installation image from USB flashdrive 
        
            1. proceed via normal LinuxCNC installation; choose some user name and password (username doesn't matter, will be deleted later on). Reboot (no need to log in via the GUI, unless you want to see the ssh host key fingerprints via `for f in /etc/ssh/ssh_host_*_key; do ssh-keygen -l -f "$f"; done`).
            
            1. install the ssh keys for root:
           
                    scp authorized_keys $username@$hostname:
                    ssh $username@$hostname
                    sudo bash -c '(umask 077 && mkdir /root/.ssh) && cp authorized_keys /root/.ssh'
                    
                then log out again.
                
            1. remove the installation user:
            
                    ssh root@$hostname
                    deluser $username
                    
                If it shows errors like "currently used by process 1234", run `killall --user $username`, then rerun the deluser command.

1. a hackspace admin: run the general Hackspace scripts on the machine (there will be no `make stage2a` here, OK?)

1. any CNC admin: run `make stage2b` (or just `make`) (TODO)


### Update all existing machines

For the CNC specific stuff:

1. any CNC admin: run `make stage2b` (or just `make`) (TODO)

For the general Hackspace stuff: the responsible Hackspace admin will
run the updates on all machines automatically (no further thinking
needed).

