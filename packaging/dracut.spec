%define dracutlibdir %{_prefix}/lib/dracut

# Variables must be defined
%define with_nbd 0

Name: dracut
Version: 024
Release: 0

Summary: Initramfs generator using udev
Group: System/Base

# The entire source code is GPLv2+
# except install/* which is LGPLv2.1+
License: GPLv2+ and LGPLv2.1+

URL: https://dracut.wiki.kernel.org/

BuildRequires: dash bash git
BuildRequires: asciidoc
BuildRequires: xsltproc

Requires: bash
Requires: coreutils
Requires: cpio
Requires: filesystem
Requires: findutils
Requires: grep
Requires: hardlink
Requires: gzip
Requires: xz
Requires: kmod-compat
Requires: sed
Requires: file
Requires: kpartx
Requires: udev > 166
Requires: kbd 
Requires: util-linux >= 2.21
Conflicts: systemd < 187

%description
Dracut contains tools to create a bootable initramfs for 2.6 Linux kernels.
Unlike existing implementations, dracut does hard-code as little as possible
into the initramfs. Dracut contains various modules which are driven by the
event-based udev. Having root on MD, DM, LVM2, LUKS is supported as well as
NFS, iSCSI, NBD, FCoE with the dracut-network package.

%package network
Summary: Dracut modules to build a dracut initramfs with network support
Requires: %{name} = %{version}-%{release}

%description network
This package requires everything which is needed to build a generic
all purpose initramfs with network support with dracut.

%package caps
Summary: Dracut modules to build a dracut initramfs which drops capabilities
Requires: %{name} = %{version}-%{release}
Requires: libcap

%description caps
This package requires everything which is needed to build an
all purpose initramfs with dracut, which drops capabilities.

%package tools
Summary: Dracut tools to build the local initramfs
Requires: %{name} = %{version}-%{release}

%description tools
This package contains tools to assemble the local initrd and host configuration.

%prep
%setup -q -n %{name}-%{version}
%build
make all

%install
make install DESTDIR=$RPM_BUILD_ROOT \
     libdir=%{_prefix}/lib \
     bindir=%{_bindir} \
%if %{defined _unitdir}
     systemdsystemunitdir=%{_unitdir} \
%endif
     sysconfdir=/etc mandir=%{_mandir}

echo "DRACUT_VERSION=%{version}-%{release}" > $RPM_BUILD_ROOT/%{dracutlibdir}/dracut-version.sh

rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/01fips
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/02fips-aesni

# we do not support dash in the initramfs
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/00dash

# remove gentoo specific modules
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/50gensplash

%if %{defined _unitdir}
# with systemd IMA and selinux modules do not make sense
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/96securityfs
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/97masterkey
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/98integrity
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/98selinux
%endif

mkdir -p $RPM_BUILD_ROOT/boot/dracut
mkdir -p $RPM_BUILD_ROOT/var/lib/dracut/overlay
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log
touch $RPM_BUILD_ROOT%{_localstatedir}/log/dracut.log
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/initramfs

install -m 0644 dracut.conf.d/suse.conf.example   $RPM_BUILD_ROOT/etc/dracut.conf.d/01-dist.conf


mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 0644 dracut.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/dracut_log

# create compat symlink
mkdir -p $RPM_BUILD_ROOT/sbin
ln -s /usr/bin/dracut $RPM_BUILD_ROOT/sbin/dracut


%files
%defattr(-,root,root,0755)
%doc README HACKING TODO COPYING AUTHORS NEWS dracut.html dracut.png dracut.svg
%{_bindir}/dracut
# compat symlink
/sbin/dracut
%{_bindir}/mkinitrd
%{_bindir}/lsinitrd
%dir %{dracutlibdir}
%dir %{dracutlibdir}/modules.d
%{dracutlibdir}/dracut-functions.sh
%{dracutlibdir}/dracut-functions
%{dracutlibdir}/dracut-version.sh
%{dracutlibdir}/dracut-logger.sh
%{dracutlibdir}/dracut-initramfs-restore
%{dracutlibdir}/dracut-install
%config(noreplace) /etc/dracut.conf
%config /etc/dracut.conf.d/01-dist.conf
%dir /etc/dracut.conf.d
%{_mandir}/man8/dracut.8*
%{_mandir}/man8/*service.8*
%{_mandir}/man8/mkinitrd.8*
%{_mandir}/man1/lsinitrd.1*
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man7/dracut.cmdline.7*
%{_mandir}/man5/dracut.conf.5*
%{dracutlibdir}/modules.d/00bootchart
%{dracutlibdir}/modules.d/04watchdog
%{dracutlibdir}/modules.d/05busybox
%{dracutlibdir}/modules.d/10i18n
%{dracutlibdir}/modules.d/30convertfs
%{dracutlibdir}/modules.d/45url-lib
%{dracutlibdir}/modules.d/50plymouth
%{dracutlibdir}/modules.d/80cms
%{dracutlibdir}/modules.d/90btrfs
%{dracutlibdir}/modules.d/90crypt
%{dracutlibdir}/modules.d/90dm
%{dracutlibdir}/modules.d/90dmraid
%{dracutlibdir}/modules.d/90dmsquash-live
%{dracutlibdir}/modules.d/90kernel-modules
%{dracutlibdir}/modules.d/90lvm
%{dracutlibdir}/modules.d/90mdraid
%{dracutlibdir}/modules.d/90multipath
%{dracutlibdir}/modules.d/90qemu
%{dracutlibdir}/modules.d/91crypt-gpg
%{dracutlibdir}/modules.d/91crypt-loop
%{dracutlibdir}/modules.d/95debug
%{dracutlibdir}/modules.d/95resume
%{dracutlibdir}/modules.d/95rootfs-block
%{dracutlibdir}/modules.d/95dasd
%{dracutlibdir}/modules.d/95dasd_mod
%{dracutlibdir}/modules.d/95fstab-sys
%{dracutlibdir}/modules.d/95zfcp
%{dracutlibdir}/modules.d/95terminfo
%{dracutlibdir}/modules.d/95udev-rules
%{dracutlibdir}/modules.d/95virtfs
%if %{undefined _unitdir}
%{dracutlibdir}/modules.d/96securityfs
%{dracutlibdir}/modules.d/97masterkey
%{dracutlibdir}/modules.d/98selinux
%{dracutlibdir}/modules.d/98integrity
%endif
%{dracutlibdir}/modules.d/97biosdevname
%{dracutlibdir}/modules.d/98ecryptfs
%{dracutlibdir}/modules.d/98pollcdrom
%{dracutlibdir}/modules.d/98syslog
%{dracutlibdir}/modules.d/98systemd
%{dracutlibdir}/modules.d/98usrmount
%{dracutlibdir}/modules.d/99base
%{dracutlibdir}/modules.d/99fs-lib
%{dracutlibdir}/modules.d/99img-lib
%{dracutlibdir}/modules.d/99shutdown
%config(noreplace) /etc/logrotate.d/dracut_log
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_localstatedir}/log/dracut.log
%dir %{_sharedstatedir}/initramfs
%if %{defined _unitdir}
%{_unitdir}/dracut-shutdown.service
%{_unitdir}/shutdown.target.wants/dracut-shutdown.service
%endif

%files network
%defattr(-,root,root,0755)
%{dracutlibdir}/modules.d/40network
%{dracutlibdir}/modules.d/95fcoe
%{dracutlibdir}/modules.d/95iscsi
%{dracutlibdir}/modules.d/90livenet
%{dracutlibdir}/modules.d/90qemu-net
%{dracutlibdir}/modules.d/95cifs
%{dracutlibdir}/modules.d/95nbd
%{dracutlibdir}/modules.d/95nfs
%{dracutlibdir}/modules.d/95ssh-client
%{dracutlibdir}/modules.d/45ifcfg
%{dracutlibdir}/modules.d/95znet


%files caps
%defattr(-,root,root,0755)
%{dracutlibdir}/modules.d/02caps

%files tools
%defattr(-,root,root,0755)
%{_mandir}/man8/dracut-catimages.8*
%{_bindir}/dracut-catimages
%dir /boot/dracut
%dir /var/lib/dracut
%dir /var/lib/dracut/overlay

