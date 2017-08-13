
# (Previously there was a setup.yaml, which was superceded by this
# Makefile because it seemed easier (perhaps just missing knowledge);
# but now that stage1 is to be done manually there's really no point
# whatsoever to a setup.yaml any more. Read README on how to use this)


all: stage2b

stage1:
	true "DO stage1 MANUALLY NOW, see README. Was: 'ansible-playbook -i inventory stage1.yaml'"

stage2b:
	ansible-playbook -i inventory stage2b.yaml
