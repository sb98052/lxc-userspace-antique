%define name lxc-userspace
%define version 1.0
%define taglevel 1

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

