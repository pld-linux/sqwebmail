#
# Conditional build:
%bcond_without	ispell	# ispell spell checker support
%bcond_with	socks	# (Courier) Socks support
%bcond_without	ssl	# HTTPS support
%bcond_with	pl	# mgt.pl beautifull patch (outdated)
#
Summary:	SqWebMail - Maildir Webmail CGI client
Summary(pl.UTF-8):	SqWebMail - Klient pocztowy CGI dla skrzynek Maildir
Name:		sqwebmail
Version:	6.1.0
Release:	1
License:	GPL v3+
Group:		Applications/Mail
Source0:	https://downloads.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	c982332b0c642468f72df28eba6c5fbc
Source1:	%{name}-cron-cleancache
Source2:	%{name}.init
Source3:	%{name}-3.4.1-mgt.pl-beautifull_patch.tgz
# Source3-md5:	90d67b405d5e9d617c9c60c88aa4acec
Source4:	%{name}-apache.conf
Patch0:		%{name}-authpam_patch
# XXX: ugly; what problem does it fix?
Patch1:		%{name}-prowizorka.patch
Patch2:		%{name}-maildir.patch
Patch3:		%{name}-init.patch
Patch4:		%{name}-disable-courierlogger-check.patch
URL:		http://www.courier-mta.org/sqwebmail/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	courier-authlib-devel >= 0.71
%{?with_socks:BuildRequires:	courier-sox-devel}
BuildRequires:	courier-unicode-devel >= 2.1
BuildRequires:	db-devel
BuildRequires:	expect
BuildRequires:	fam-devel
# or gnupg2 --with-gpg2
BuildRequires:	gnupg >= 1.0.4
BuildRequires:	libidn2-devel >= 0.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	openldap-devel
BuildRequires:	pcre2-8-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	procps
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sysconftool
Requires(post,preun):	/sbin/chkconfig
%{?with_ssl:Requires:	apache(mod_ssl)}
Requires:	courier-authlib >= 0.71
Requires:	courier-unicode >= 2.1
Requires:	crondaemon
Requires:	expect
Requires:	filesystem >= 3.0-11
Requires:	gnupg >= 1.0.4
%{?with_ispell:Requires:	ispell}
Requires:	mailcap
Requires:	rc-scripts
Requires:	webapps
Requires:	webserver = apache
Conflicts:	apache-base < 2.2.0-8
Conflicts:	apache1 < 1.3.34-5.11
Conflicts:	courier-imap < 5
Conflicts:	courier-imapd < 1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localstatedir	/var/spool/sqwebmail
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%define		cgibindir	%{_prefix}/lib/cgi-bin
%define		imagedir	%{_datadir}/sqwebmail/images
%define		imageurl	/webmail

%define		cacheowner	bin
%define		sqwebmailowner	root
%define		sqwebmailgroup	mail
%define		sqwebmailperm	555

%description
SqWebMail is a Webmail CGI for Maildir mailboxes.

%description -l pl.UTF-8
SqWebMail jest klientem pocztowym CGI dla skrzynek Maildir.

%package calendar
Summary:	SqWebMail calendar
Summary(pl.UTF-8):	Kalendarz dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}-%{release}

%description calendar
SqWebMail Calendar.

%description calendar -l pl.UTF-8
Kalendarz SqWebMaila.

%package pl_html
Summary:	SqWebMail - Polish translation
Summary(pl.UTF-8):	Sqwebmail - polska wersja interfejsu
Group:		Applications/Mail
Requires:	%{name} = %{version}-%{release}

%description pl_html
Polish translation.

%description pl_html -l pl.UTF-8
Polskie tłumaczenie interfejsu.

%prep
%setup -q %{?with_pl:-a3}
cp -p %{SOURCE2} sqwebmail.init.in
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
for d in $(sed -ne 's/.*AC_CONFIG_SUBDIRS(\([^)]*\))/\1/p' configure.ac) . ; do
	cd "$d"
	sed -i -e '/_[L]DFLAGS=-static/d' Makefile.am
	%{__aclocal}
	%{__autoconf}
	%{__autoheader}
	%{__automake}
        cd -
done
# depcomp is used by subdirs, but not from top automake, need to install manually
cp -f /usr/share/automake/depcomp .

%configure \
	--enable-cgibindir=%{cgibindir} \
	%{?with_ssl:--enable-https} \
	--enable-imagedir=%{imagedir} \
	--enable-imageurl=%{imageurl} \
	--enable-mimetypes=/etc/mime.types \
	--with-cachedir=%{_localstatedir}/tmp \
	--with-cacheowner=%{cacheowner} \
	--with-db=db \
	--with-formdata \
	%{?with_ispell:--with-ispell=/usr/bin/ispell} \
	--with-mailer=/usr/lib/sendmail \
	--with-notice=unicode \
	--with-piddir=/var/run \
	%{!?with_socks:--without-socks}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{shared,shared.tmp} \
	$RPM_BUILD_ROOT/etc/{cron.hourly,pam.d,rc.d/init.d}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with pl}
install -d $RPM_BUILD_ROOT%{_datadir}/sqwebmail/html/pl-pl
cp -p sqwebmail-3.4.1-mgt.pl-beautifull_patch/html/pl-pl/* $RPM_BUILD_ROOT%{_datadir}/sqwebmail/html/pl-pl
%endif

install libs/gpglib/webgpg $RPM_BUILD_ROOT%{_sbindir}

# make config file
./sysconftool $RPM_BUILD_ROOT%{_sysconfdir}/*.dist
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/*.dist
echo net >$RPM_BUILD_ROOT%{_sysconfdir}/calendarmode
%if %{with ispell}
touch $RPM_BUILD_ROOT%{_datadir}/sqwebmail/html/en/ISPELLDICT
%endif

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.hourly/sqwebmail-cron-cleancache
install sqwebmail.init $RPM_BUILD_ROOT/etc/rc.d/init.d/sqwebmail
# obsoleted by .init script
%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/sqwebmaild.rc

# pam
cp -p libs/sqwebmail/sqwebmail.pamconf $RPM_BUILD_ROOT/etc/pam.d/webmail
cp -p libs/sqwebmail/sqwebmail.pamconf $RPM_BUILD_ROOT/etc/pam.d/calendar

# for apache
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

cp -p libs/gpglib/README.html README_gpglib.html
cp -p libs/pcp/README.html README_pcp.html

# in courier-imap
%{__rm} $RPM_BUILD_ROOT%{_sbindir}/sharedindex{install,split}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -L %{_datadir}/sqwebmail/html/en ] || ln -fs en-us %{_datadir}/sqwebmail/html/en
/sbin/chkconfig --add sqwebmail
%service sqwebmail restart

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del sqwebmail
	%service sqwebmail stop
	[ ! -L %{_datadir}/sqwebmail/html/en ] || rm -f %{_datadir}/sqwebmail/html/en
fi

%post calendar
if [ -f /var/run/sqwebmaild.pid.pcp ]; then
	%{_sbindir}/courierlogger -pid=/var/run/sqwebmaild.pid.pcp -stop
	rm -f /var/run/sqwebmaild.pid.pcp
	%{_sbindir}/courierlogger -pid=/var/run/sqwebmaild.pid.pcp -start \
		%{_libexecdir}/sqwebmail/pcpd server
else
	# FIXME: why not just restart it? %%service -q sqwebmail restart
	if [ -f /var/lock/subsys/sqwebmail ]; then
		echo
		echo 'Type "/sbin/service sqwebmail restart" to start sqwebmail with calendar'
		echo
	else
		echo
		echo 'Type "/sbin/service sqwebmail start" to start sqwebmail with calendar'
		echo
	fi
fi

%preun calendar
if [ "$1" = "0" ]; then
	if [ -f /var/run/sqwebmaild.pid.pcp ]; then
		%{_sbindir}/courierlogger -pid=/var/run/sqwebmaild.pid.pcp -stop
		rm -f /var/run/sqwebmaild.pid.pcp
	fi
fi

%post pl_html
[ -L %{_datadir}/sqwebmail/html/pl ] || ln -fs pl-pl %{_datadir}/sqwebmail/html/pl
echo "echo 'pl-pl' > %{_datadir}/sqwebmail/html/en/LANGUAGE"

%preun pl_html
[ ! -L %{_datadir}/sqwebmail/html/pl ] || rm -f %{_datadir}/sqwebmail/html/pl

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerpostun -- %{name} < 6
# 5.0.4-1.1
# rescue app configs
for i in ldapaddressbook sqwebmaild; do
	if [ -f /etc/%{name}/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/$i{,.rpmnew}
		mv -f /etc/%{name}/$i.rpmsave %{_sysconfdir}/$i
	fi
done

if [ -f /etc/%{name}/apache-%{name}.conf.rpmsave ]; then
	if [ -d /etc/apache/webapps.d ]; then
		cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
		cp -f /etc/%{name}/apache-%{name}.conf.rpmsave %{_sysconfdir}/apache.conf
	fi

	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
		cp -f /etc/%{name}/apache-%{name}.conf.rpmsave %{_sysconfdir}/httpd.conf
	fi
	rm -f /etc/%{name}/apache-%{name}.conf.rpmsave
fi

if [ -L /etc/apache/conf.d/99_%{name}.conf ]; then
	rm -f /etc/apache/conf.d/99_%{name}.conf
	apache_reload=1
fi
if [ -L /etc/httpd/httpd.conf/99_%{name}.conf ]; then
	rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	httpd_reload=1
fi

if [ "$httpd_reload" ]; then
	/usr/sbin/webapp register httpd %{_webapp}
	%service httpd reload
fi
if [ "$apache_reload" ]; then
	/usr/sbin/webapp register apache %{_webapp}
	%service apache reload
fi

# 6
%banner -e sqwebmail-unicode <<EOF
WARNING: you have to convert any existing maildirs to Unicode naming scheme.
See INSTALL file for details.
EOF

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING INSTALL NEWS README README_gpglib.html libs/sqwebmail/{BUGS,ChangeLog,SECURITY,TODO} libs/maildir/README.*.html
%attr(755,root,root) %{_sbindir}/webgpg
%attr(755,root,root) %{cgibindir}/sqwebmail

%dir %{_libexecdir}/sqwebmail
%attr(755,root,root) %{_libexecdir}/sqwebmail/deliverquota
%attr(755,root,root) %{_libexecdir}/sqwebmail/maildirmake
%attr(755,root,root) %{_libexecdir}/sqwebmail/makemime
%attr(755,root,root) %{_libexecdir}/sqwebmail/reformime
%attr(755,root,root) %{_libexecdir}/sqwebmail/sqwebmaild
%attr(2755,%{sqwebmailowner},%{sqwebmailgroup}) %{_libexecdir}/sqwebmail/sqwebpasswd

%dir %{_sysconfdir}
%attr(755,daemon,daemon) %dir %{_sysconfdir}/shared
%attr(755,daemon,daemon) %dir %{_sysconfdir}/shared.tmp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ldapaddressbook
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sqwebmaild
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf

%dir %{_datadir}/sqwebmail
%dir %{_datadir}/sqwebmail/html
%ghost %{_datadir}/sqwebmail/html/en
%dir %{_datadir}/sqwebmail/html/en-us
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/en-us/CHARSET
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/en-us/LANGUAGE
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/en-us/LANGUAGE_PREF
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/en-us/LOCALE
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/en-us/TIMEZONELIST
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/en-us/ISPELLDICT
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/webmail
%{_datadir}/sqwebmail/html/en-us/*.html
%{_datadir}/sqwebmail/html/en-us/*.txt
%{imagedir}
%attr(755,root,root) %{_datadir}/sqwebmail/ldapsearch
%attr(755,root,root) %{_datadir}/sqwebmail/webgpg
%attr(755,root,root) %{_datadir}/sqwebmail/sendit.sh
%attr(755,root,root) %{_datadir}/sqwebmail/cleancache.pl

%attr(754,root,root) /etc/rc.d/init.d/sqwebmail
%attr(755,root,root) /etc/cron.hourly/sqwebmail-cron-cleancache

%attr(771,root,daemon) %dir %{_localstatedir}
%attr(700,%{cacheowner},root) %dir %{_localstatedir}/tmp

%files calendar
%defattr(644,root,root,755)
%doc README_pcp.html
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/calendarmode
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/calendar
%attr(755,root,root) %{_libexecdir}/sqwebmail/pcpd
%attr(751,bin,bin) %dir %{_localstatedir}/calendar
%attr(700,bin,bin) %dir %{_localstatedir}/calendar/localcache
%attr(750,bin,bin) %dir %{_localstatedir}/calendar/private
%attr(755,bin,bin) %dir %{_localstatedir}/calendar/public

%if %{with pl}
%files pl_html
%defattr(644,root,root,755)
%ghost %{_datadir}/sqwebmail/html/pl
%dir %{_datadir}/sqwebmail/html/pl-pl
%{_datadir}/sqwebmail/html/pl-pl/*.html
%{_datadir}/sqwebmail/html/pl-pl/*.txt
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/pl-pl/CHARSET
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/pl-pl/LANGUAGE
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/pl-pl/LANGUAGE_PREF
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/pl-pl/LOCALE
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/pl-pl/TIMEZONELIST
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/pl-pl/ISPELLDICT
%endif
