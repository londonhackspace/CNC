sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get install linux-image-rt-686-pae


- name: restart machine
  command: shutdown -r now "Ansible updates triggered"
  async: 0
  poll: 0
  ignore_errors: true