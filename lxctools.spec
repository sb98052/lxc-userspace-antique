%define name lxctools
%define version 0.1
%define taglevel 1

%define percent %
%define braop \{
%define bracl \}
%define kernel_version %( rpm -q --qf %{percent}%{braop}version%{bracl} kernel-headers )
%define kernel_release %( rpm -q --qf %{percent}%{braop}release%{bracl} kernel-headers )
%define kernel_arch %( rpm -q --qf %{percent}%{braop}arch%{bracl} kernel-headers )

# this is getting really a lot of stuff, could be made simpler probably
%define release %{kernel_version}.%{kernel_release}.%{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}

%define kernel_id %{kernel_version}-%{kernel_release}.%{kernel_arch}
%define kernelpath /usr/src/kernels/%{kernel_id}


Vendor: PlanetLab
Packager: PlanetLab Central <support@planet-lab.org>
Distribution: PlanetLab %{plrelease}
URL: %{SCMURL}
Requires: kernel = %{kernel_version}-%{kernel_release}

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
/usr/sbin
/lib

%postun

%changelog
