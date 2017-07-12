
# This is stupid of course (or not?) since there's setup.yaml which
# should do the same. ?


all: stage2b

stage1:
	true "DO stage1 MANUALLY NOW, see README. Was: 'ansible-playbook -i inventory stage1.yaml'"

stage2b:
	ansible-playbook -i inventory stage2b.yaml
