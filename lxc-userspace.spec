%define name lxc-userspace
%define version 1.0
%define taglevel 9

%define percent %
%define braop \{
%define bracl \}

# this is getting really a lot of stuff, could be made simpler probably
%define release %{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}

Vendor: PlanetLab
Packager: PlanetLab Central <support@planet-lab.org>
Distribution: PlanetLab %{plrelease}
URL: %{SCMURL}

Summary: Userspace tools for switching between lxc containers
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Group: System Environment/Kernel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: lxc-userspace-%{version}.tar.gz
Requires: binutils

Obsoletes: lxctools

%description
Userspace tools for switching between lxc containers.

%prep 
%setup -q

%build
make 

%install
mkdir -p $RPM_BUILD_ROOT/usr/sbin
install -D -m 755 vsh $RPM_BUILD_ROOT/usr/sbin/vsh
install -D -m 755 lxcsu $RPM_BUILD_ROOT/usr/sbin/lxcsu
install -D -m 755 lxcsu-internal $RPM_BUILD_ROOT/usr/sbin/lxcsu-internal
chmod u+s $RPM_BUILD_ROOT/usr/sbin/lxcsu
cp build/lib*/setns.so $RPM_BUILD_ROOT/usr/sbin

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/sbin/*

%post
chmod u+s /usr/sbin/vsh

%postun

%changelog
* Fri Mar 21 2014 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - lxc-userspace-1.0-9
- does not rely on capsh (actually this was the one in the sliver)
- use native capability dropping instead
- provides new slicesu binary
- suitable for libvirt-1.1 and above

* Fri Sep 20 2013 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - lxc-userspace-1.0-8
- fix vsh permissions

* Sat Aug 31 2013 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - lxc-userspace-1.0-7
- perform vsys sysctl inside of container
- remove unnecessary proc remounts
- prevent setting LD_PRELOAD if the library doesn't exist in image
- add --noslicehome option
- check /etc/lxcsu_default for default arguments
- fix permissions
- support conventional invocation of make

* Sun Jul 14 2013 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - lxc-userspace-1.0-6
- merge back lxcsu and -internal into a single source file
- capsh --uid instead of --user that was not yet supported in f12 (hopefully tmp)

* Wed Jul 03 2013 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - lxc-userspace-1.0-5
- entering in a slice now correctly ends up with right uid and pwd
- make sync

* Mon Jul 01 2013 Sapan Bhatia <sapanb@cs.princeton.edu> - lxc-userspace-1.0-4
- Bug fixes:
- - lxcsu <slice_name> works again
- - pid namespace issue that would let slices see all processes

* Fri Jun 28 2013 Sapan Bhatia <sapanb@cs.princeton.edu> - lxc-userspace-1.0-3
- Fixed bug that would let slices see all processes in root context.

* Wed Jun 26 2013 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - lxc-userspace-1.0-2
- split into lxcsu{,-internal}

* Wed Jun 05 2013 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - lxc-userspace-1.0-1
- rename module and package from lxctools into lxc-userspace

* Mon Jun 03 2013 Sapan Bhatia <sapanb@cs.princeton.edu> - lxctools-0.9-8
- - Upgraded code for compatibility with kernel 3.6.9
- - Obsoleted modules for switching into mnt and pid namespaces
- - Added command to mount /proc if not mounted

* Wed May 29 2013 Andy Bavier <acb@cs.princeton.edu> - lxctools-0.9-7
- Use ArgumentParser, fix issue with sensing arch

* Wed May 29 2013 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - lxctools-0.9-6
- implements vm's arch

* Tue Apr 23 2013 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - lxctools-0.9-5
- more flexible and more robust lxcsu

* Thu Mar 07 2013 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - lxctools-0.9-4
- nicer polish to lxcsu returning the right thing

* Mon Mar 04 2013 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - lxctools-0.9-3
- lxcsu to propagate its forked process's return code

* Fri Feb 22 2013 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - lxctools-0.9-2
- various fixes

