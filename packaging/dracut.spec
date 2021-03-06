%define dracutlibdir %{_prefix}/lib/dracut

# Variables must be defined
%define with_nbd 0

Name:           dracut
Version:        032
Release:        0
Summary:        Initramfs generator using udev
Group:          Base/Startup
# The entire source code is GPL-2.0+
# except install/* which is LGPL-2.1+
License:        GPL-2.0+ and LGPL-2.1+
Url:            https://dracut.wiki.kernel.org/
Source0:        %{name}-%{version}.tar.xz
Source1001: 	dracut.manifest
BuildRequires:  asciidoc
BuildRequires:  bash
BuildRequires:  dash
BuildRequires:  git
BuildRequires:  xsltproc
Requires:       bash
Requires:       coreutils
Requires:       cpio
Requires:       file
Requires:       filesystem
Requires:       findutils
Requires:       grep
Requires:       gzip
Requires:       hardlink
Requires:       kbd
Requires:       kmod-compat
Requires:       kpartx
Requires:       sed
Requires:       udev > 166
Requires:       util-linux >= 2.21
Requires:       xz
Conflicts: systemd < 187

%description
Dracut contains tools to create a bootable initramfs for 2.6 Linux kernels.
Unlike existing implementations, dracut does hard-code as little as possible
into the initramfs. Dracut contains various modules which are driven by the
event-based udev. Having root on MD, DM, LVM2, LUKS is supported as well as
NFS, iSCSI, NBD, FCoE with the dracut-network package.

%package network
Summary:        Dracut modules to build a dracut initramfs with network support
Requires:       %{name} = %{version}

%description network
This package requires everything which is needed to build a generic
all purpose initramfs with network support with dracut.

%package caps
Summary:        Dracut modules to build a dracut initramfs which drops capabilities
Requires:       %{name} = %{version}
Requires:       libcap

%description caps
This package requires everything which is needed to build an
all purpose initramfs with dracut, which drops capabilities.

%package tools
Summary:        Dracut tools to build the local initramfs
Requires:       %{name} = %{version}

%description tools
This package contains tools to assemble the local initrd and host configuration.

%prep
%setup -q
cp %{SOURCE1001} .
%build
make all

%install
make install DESTDIR=%{buildroot} \
     libdir=%{_prefix}/lib \
     bindir=%{_bindir} \
%if %{defined _unitdir}
     systemdsystemunitdir=%{_unitdir} \
%endif
     sysconfdir=/etc mandir=%{_mandir}

echo "DRACUT_VERSION=%{version}-%{release}" > %{buildroot}/%{dracutlibdir}/dracut-version.sh

rm -fr %{buildroot}/%{dracutlibdir}/modules.d/01fips
rm -fr %{buildroot}/%{dracutlibdir}/modules.d/02fips-aesni


# remove gentoo specific modules
rm -fr %{buildroot}/%{dracutlibdir}/modules.d/50gensplash

%if %{defined _unitdir}
# with systemd IMA and selinux modules do not make sense
rm -fr %{buildroot}/%{dracutlibdir}/modules.d/96securityfs
rm -fr %{buildroot}/%{dracutlibdir}/modules.d/97masterkey
rm -fr %{buildroot}/%{dracutlibdir}/modules.d/98integrity
rm -fr %{buildroot}/%{dracutlibdir}/modules.d/98selinux
%endif

mkdir -p %{buildroot}/boot/dracut
mkdir -p %{buildroot}%{_localstatedir}/lib/dracut/overlay
mkdir -p %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/log/dracut.log
mkdir -p %{buildroot}%{_sharedstatedir}/initramfs

install -m 0644 dracut.conf.d/suse.conf.example   %{buildroot}%{_sysconfdir}/dracut.conf.d/01-dist.conf


mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 0644 dracut.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/dracut_log


%files
%manifest %{name}.manifest
%defattr(-,root,root,0755)
%license COPYING
%{_bindir}/dracut
# compat symlink
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
%config(noreplace) %{_sysconfdir}/dracut.conf
%config %{_sysconfdir}/dracut.conf.d/01-dist.conf
%dir %{_sysconfdir}/dracut.conf.d
%{_mandir}/man8/dracut.8*
%{_mandir}/man8/*service.8*
%{_mandir}/man8/mkinitrd.8*
%{_mandir}/man1/lsinitrd.1*
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man7/dracut.bootup.7*
%{_mandir}/man7/dracut.cmdline.7*
%{_mandir}/man5/dracut.conf.5*
%{dracutlibdir}/modules.d/00dash
%{dracutlibdir}/modules.d/00bootchart
%{dracutlibdir}/modules.d/00systemd-bootchart/module-setup.sh
%{dracutlibdir}/modules.d/03rescue/module-setup.sh
%{dracutlibdir}/modules.d/04watchdog
%{dracutlibdir}/modules.d/05busybox
%{dracutlibdir}/modules.d/10i18n
%{dracutlibdir}/modules.d/30convertfs
%{dracutlibdir}/modules.d/45url-lib
%{dracutlibdir}/modules.d/50plymouth
%{dracutlibdir}/modules.d/50drm/module-setup.sh
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
%{dracutlibdir}/modules.d/00bash/module-setup.sh
%{dracutlibdir}/modules.d/03modsign/load-modsign-keys.sh
%{dracutlibdir}/modules.d/03modsign/module-setup.sh
%{dracutlibdir}/modules.d/90bcache/module-setup.sh
%config(noreplace) %{_sysconfdir}/logrotate.d/dracut_log
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_localstatedir}/log/dracut.log
%dir %{_sharedstatedir}/initramfs
%if %{defined _unitdir}
%{_unitdir}/dracut-shutdown.service
%{_unitdir}/shutdown.target.wants/dracut-shutdown.service
%{_unitdir}/dracut-cmdline.service
%{_unitdir}/dracut-initqueue.service
%{_unitdir}/dracut-mount.service
%{_unitdir}/dracut-pre-mount.service
%{_unitdir}/dracut-pre-pivot.service
%{_unitdir}/dracut-pre-trigger.service
%{_unitdir}/dracut-pre-udev.service
%{_unitdir}/initrd.target.wants/dracut-cmdline.service
%{_unitdir}/initrd.target.wants/dracut-initqueue.service
%{_unitdir}/initrd.target.wants/dracut-mount.service
%{_unitdir}/initrd.target.wants/dracut-pre-mount.service
%{_unitdir}/initrd.target.wants/dracut-pre-pivot.service
%{_unitdir}/initrd.target.wants/dracut-pre-trigger.service
%{_unitdir}/initrd.target.wants/dracut-pre-udev.service
%endif
/usr/lib/kernel/install.d/50-dracut.install
/usr/lib/kernel/install.d/51-dracut-rescue.install
%{_datadir}/bash-completion/completions/dracut
%{_datadir}/bash-completion/completions/lsinitrd

%files network
%manifest %{name}.manifest
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
%manifest %{name}.manifest
%defattr(-,root,root,0755)
%{dracutlibdir}/modules.d/02caps

%files tools
%manifest %{name}.manifest
%defattr(-,root,root,0755)
%{_mandir}/man8/dracut-catimages.8*
%{_bindir}/dracut-catimages
%dir /boot/dracut
%dir %{_localstatedir}/lib/dracut
%dir %{_localstatedir}/lib/dracut/overlay

