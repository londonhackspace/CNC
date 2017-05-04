
# This is stupid of course (or not?) since there's setup.yaml which
# should do the same. ?


all: stage1 stage2

stage1:
	ansible-playbook -i inventory stage1.yaml

stage2:
	ansible-playbook -i inventory stage2.yaml
