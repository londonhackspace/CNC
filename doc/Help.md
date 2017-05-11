# Help

## Debian 

* The command(s) to run if package installation is interrupted and apt won't proceed when re-run:

        dpkg --configure -a  # I think apt-get -f install runs this automatically though
        apt-get -f install


## Ansible Debugging

* "some modules have built-in debug logging that can be activated by running ansible with ANSIBLE_DEBUG=1, but aside from that, you can edit the module code to add debug logging or run it through the python debugger"
    * run `ANSIBLE_DEBUG=1 ansible-playbook ansible_playbook.yaml -i hosts`, does nothing for this

* does that work, how is it meant?

    > &lt;bcoca> debug: var=registerdvarname will show everything


## Remote maintenance

You can ssh into `chomsky.london.hackspace.org.uk`, then access other machines from there.

Although chomsky doesn't have ansible installed. XXX TODO.
