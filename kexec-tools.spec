Name: kexec-tools
Version: 1.101
Release: 3
License: GPL
Group: Applications/System
Summary: The kexec/kdump userspace component.
ExclusiveArch: %{ix86}
Source0: %{name}-%{version}.tar.gz
Source1: kdump.init
Source2: kdump.sysconfig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

#
# Patches 0 through 100 are meant for x86 kexec-tools enablement
#
Patch1: kexec-tools-1.101-kdump.patch

#
# Patches 101 through 200 are meant for x86_64 kexec-tools enablement
#

#
# Patches 201 through 300 are meant for ia64 kexec-tools enablement
#

#
# Patches 301 through 400 are meant for ppc64 kexec-tools enablement
#

%description
kexec-tools provides /sbin/kexec binary that facilitates a new
kernel to boot using the kernel's kexec feature either on a
normal or a panic reboot. This package contains the /sbin/kexec
binary and ancillary utilities that together form the userspace
component of the kernel's kexec feature.

%prep
%setup -q -n %{name}-%{version}
rm -f ../kexec-tools-1.101.spec
%patch1 -p1

cp $RPM_SOURCE_DIR/kdump.init .
cp $RPM_SOURCE_DIR/kdump.sysconfig .

%build
%configure
rm -f kexec-tools.spec.in
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p -m755 $RPM_BUILD_ROOT/etc/sysconfig
install -m 644 kdump.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/kdump
install -m 755 kdump.init $RPM_BUILD_ROOT/etc/rc.d/init.d/kdump

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add kdump

%postun
if [ "$1" -ge 1 ]; then
	/sbin/service kdump condrestart > /dev/null 2>&1 || :
fi

%preun
if [ "$1" = 0 ]; then
	/sbin/service kdump stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del kdump
fi
exit 0

%files
%defattr(-,root,root,-)
%{_sbindir}/kexec
%{_sbindir}/kdump
%{_libdir}/kexec-tools/kexec_test
%config(noreplace,missingok) /etc/sysconfig/kdump
%config /etc/rc.d/init.d/kdump
%doc News
%doc COPYING
%doc TODO

%changelog
* Fri Sep 23 2005 Jeff Moyer <jmoyer@redhat.com> - 1.101-3
- Add a kdump sysconfig file and init script
- Spec file additions for pre/post install/uninstall

* Thu Aug 25 2005 Jeff Moyer <jmoyer@redhat.com>
- Initial prototype for RH/FC5
