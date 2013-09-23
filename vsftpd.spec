Summary:	vsftpd - Very Secure FTP Daemon
Name:		vsftpd
Version:	3.0.2
Release:	2
License:	GPL v2
Group:		Daemons
Source0:	https://security.appspot.com/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	8b00c749719089401315bd3c44dddbb2
Source1:	%{name}.pamd
Source2:	%{name}-ftpusers
Source3:	%{name}@.service
# Source3-md5:	75df14e1615ae074790c47d093934959
Source4:	%{name}.socket
Patch0:		%{name}-config_dir.patch
Patch1:		%{name}-config.patch
URL:		http://vsftpd.beasts.org/
BuildRequires:	libcap-devel
BuildRequires:	pam-devel
Requires(post,preun,postun):	systemd-units
Provides:	ftpserver
Requires:	pam
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ftpdir	/home/services/ftp

%description
A Very Secure FTP Daemon - written from scratch - by Chris "One Man
Security Audit Team" Evans.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

sed -i -e "/^#define VSF_BUILD_TCPWRAPPERS/d" builddefs.h

%build
%{__make} \
	CC="%{__cc}"			\
	CFLAGS="%{rpmcflags} -fPIE"	\
	LDFLAGS="-fPIE -pie %{rpmldflags} -Wl,-z,now"	\
	LINK=""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT/etc/{pam.d,sysconfig/rc-inetd,logrotate.d,vsftpd} \
	$RPM_BUILD_ROOT%{systemdunitdir} \
	$RPM_BUILD_ROOT{%{ftpdir}/pub/incoming,/var/log}

install vsftpd $RPM_BUILD_ROOT%{_sbindir}/vsftpd
install vsftpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/vsftpd.conf
install vsftpd.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/vsftpd.conf.5
install vsftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/vsftpd.8
install RedHat/vsftpd.log $RPM_BUILD_ROOT/etc/logrotate.d/vsftpd

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/ftp
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/ftpusers
install %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}

:> $RPM_BUILD_ROOT/var/log/vsftpd.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post %{name}.socket

%preun
%systemd_preun %{name}.socket

%postun
%systemd_postun

%files
%defattr(644,root,root,755)
%doc AUDIT BENCHMARKS BUGS Changelog FAQ README README.ssl REWARD SIZE SPEED TODO TUNING EXAMPLE SECURITY

%dir %{_sysconfdir}/vsftpd
%dir %{ftpdir}
%dir %{ftpdir}/pub

%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vsftpd/ftpusers
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vsftpd/vsftpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/vsftpd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/ftp

%{systemdunitdir}/vsftpd.socket
%{systemdunitdir}/vsftpd@.service

%attr(640,root,root) %ghost /var/log/vsftpd.log

%attr(755,root,root) %{_sbindir}/vsftpd

%attr(775,root,ftp) %dir %{ftpdir}/pub/incoming
%{_mandir}/man5/vsftpd.conf.5*
%{_mandir}/man8/vsftpd.8*

