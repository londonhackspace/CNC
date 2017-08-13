# To do to get automatic stage1 to work

* the parallel port does not work when setting up a machine that way. We haven't figured out why, it might be a package missing (that the Debian installer installs, but the debootstrap based script doesn't).
* scripts/stage1 hard codes the disk name (`/dev/sda`). Should this be a parameter, or should it ask for confirmation? By way of a wrapper script around calling Ansible?
* `wait_for` for waiting after reboot still fails to work properly (...?, and how to handle change of ssh host key)

## Cosmetics

* Is there an ansible module to install packages? Doesn't really matter either way though since LinuxCNC is Debian only anyway.

