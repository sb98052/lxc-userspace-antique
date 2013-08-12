all: vsh setns.so
	
vsh: vsh.c
	gcc vsh.c -o vsh

setns: setns.c
	python setup.py build
	

########## sync
# for use with the test framework; push local stuff on a test node
# howto use: go on testmaster in the build you want to use and just run
# $ exp
# cut'n paste the result in a terminal in your working dir, e.g. (although all are not required)
# $ export BUILD=2013.07.02--lxc18
# $ export PLCHOSTLXC=gotan.pl.sophia.inria.fr
# $ export GUESTNAME=2013.07.02--lxc18-1-vplc01
# $ export GUESTHOSTNAME=vplc01.pl.sophia.inria.fr
# $ export KVMHOST=kvm64-6.pl.sophia.inria.fr
# $ export NODE=vnode01.pl.sophia.inria.fr
# and then just run
# $ make sync
# this will attempt to compile vsh from vsh.c (and will push Makefile.vsh in /usr/sbin/)
# so you might have to yum install gcc

LOCAL_RSYNC_EXCLUDES	:= --exclude '*.pyc' 
RSYNC_EXCLUDES		:= --exclude .git  --exclude .svn --exclude '*~' --exclude TAGS $(LOCAL_RSYNC_EXCLUDES)
RSYNC_COND_DRY_RUN	:= $(if $(findstring n,$(MAKEFLAGS)),--dry-run,)
RSYNC			:= rsync -e "ssh -i $(NODE).key.rsa" -a -v $(RSYNC_COND_DRY_RUN) $(RSYNC_EXCLUDES)

ifdef NODE
NODEURL:=root@$(NODE):/
endif

sync: $(NODE).key.rsa
ifeq (,$(NODEURL))
	@echo "sync: You must define NODE on the command line"
	@echo "  e.g. make sync NODE=vnode01.inria.fr"
	@exit 1
else
	+$(RSYNC) ./lxcsu ./lxcsu-internal ./vsh.c ./Makefile.vsh $(NODEURL)/usr/sbin/
	ssh -i $(NODE).key.rsa root@$(NODE) make -C /usr/sbin -f Makefile.vsh vsh
	ssh -i $(NODE).key.rsa root@$(NODE) chown root:root /usr/sbin/lxcsu /usr/sbin/vsh
	ssh -i $(NODE).key.rsa root@$(NODE) chmod u+s /usr/sbin/lxcsu /usr/sbin/vsh
endif

### fetching the key

TESTMASTER ?= testmaster.onelab.eu

ifdef BUILD
KEYURL:=root@$(TESTMASTER):$(BUILD)/keys/key_admin.rsa
endif

key: $(NODE).key.rsa

$(NODE).key.rsa:
ifeq (,$(KEYURL))
	@echo "sync: fetching $@ - You must define TESTMASTER, BUILD and NODE on the command line"
	@echo "  e.g. make sync TESTMASTER=testmaster.onelab.eu BUILD=2010.01.22--1l-f8-32 NODE=vnode01.inria.fr"
	@echo "  note that for now all test builds use the same key, so any BUILD would do"
	@exit 1
else
	@echo "FETCHING key"
	+scp $(KEYURL) $@
endif

### poor man's install

install: setns vsh
	mkdir -p /usr/sbin
	install -D -m 755 vsh /usr/sbin/vsh
	install -D -m 755 lxcsu /usr/sbin/lxcsu
	install -D -m 755 lxcsu-internal /usr/sbin/lxcsu-internal
	chmod u+s /usr/sbin/lxcsu
	cp build/lib*/setns.so /usr/sbin
