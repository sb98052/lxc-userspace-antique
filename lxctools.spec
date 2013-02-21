%define name lxctools
%define version 0.9
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
Source0: lxctools-%{version}.tar.gz

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
