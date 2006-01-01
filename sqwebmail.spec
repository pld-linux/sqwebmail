#
# Conditional build:
%bcond_without	ispell
%bcond_without	ssl
%bcond_with	pl
#
%include	/usr/lib/rpm/macros.perl
Summary:	SqWebMail - Maildir Webmail CGI client
Summary(pl):	SqWebMail - Klient pocztowy CGI dla skrzynek Maildir
Name:		sqwebmail
Version:	5.0.4
Release:	1.6
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	fee97b3546b954f0307e2d8963be7498
Source1:	%{name}-cron-cleancache
Source2:	%{name}.init
Source3:	%{name}-3.4.1-mgt.pl-beautifull_patch.tgz
Source4:	%{name}-apache.conf
Patch0:		%{name}-authpam_patch
Patch1:		%{name}-prowizorka.patch
Patch2:		%{name}-maildir.patch
Patch3:		%{name}-init.patch
Patch4:		%{name}-sec_fix.patch
URL:		http://www.courier-mta.org/sqwebmail/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	courier-authlib-devel >= 0.57
BuildRequires:	db-devel
BuildRequires:	expect
BuildRequires:	fam-devel
BuildRequires:	gnupg >= 1.0.4
# perhaps only because of test sources written in C, but with ".C" extension(?)
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	procps
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.264
BuildRequires:	sysconftool
Requires(post,preun):	/sbin/chkconfig
Requires:	FHS >= 2.3-12
%{?with_ssl:Requires:	apache(mod_ssl)}
Requires:	crondaemon
Requires:	expect
Requires:	gnupg >= 1.0.4
%{?with_ispell:Requires:	ispell}
Requires:	mailcap
Requires:	rc-scripts
Requires:	webserver = apache
Conflicts:	apache-base < 2.2.0-8
Conflicts:	apache1 < 1.3.34-5.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_libexecdir		/usr/%{_lib}
%define	_localstatedir		/var/spool/sqwebmail
%define	_webapps	/etc/webapps
%define	_webapp		%{name}
%define	_sysconfdir	%{_webapps}/%{_webapp}

%define	cgibindir		%{_prefix}/lib/cgi-bin
%define	imagedir		%{_datadir}/sqwebmail/images
%define	imageurl		/webmail

%define	cacheowner		bin
%define	sqwebmailowner		root
%define	sqwebmailgroup		mail
%define	sqwebmailperm		555

%description
SqWebMail is a Webmail CGI for Maildir mailboxes.

%description -l pl
SqWebMail jest klientem pocztowym CGI dla skrzynek Maildir.

%package calendar
Summary:	SqWebMail calendar
Summary(pl):	Kalendarz dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}-%{release}

%description calendar
SqWebMail Calendar.

%description calendar -l pl
Kalendarz SqWebMaila.

%package pl_html
Summary:	SqWebMail - Polish translation
Summary(pl):	Sqwebmail - polska wersja interfejsu
Group:		Applications/Mail
Requires:	%{name} = %{version}-%{release}

%description pl_html
Polish translation.

%description pl_html -l pl
Polskie t³umaczenie interfejsu.

%prep
%setup -q
install %{SOURCE2} sqwebmail.init.in
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
# Change Makefile.am files and force recreate Makefile.in's.
OLDDIR=`pwd`
find -type f -a \( -name configure.in -o -name configure.ac \) | while read FILE; do
        cd "`dirname "$FILE"`"

        if [ -f Makefile.am ]; then
                sed -i -e '/_[L]DFLAGS=-static/d' Makefile.am
        fi

        %{__libtoolize}
        %{__aclocal}
        %{__autoconf}
        %{__autoheader}
        %{__automake}

        cd "$OLDDIR"
done

%configure \
	--with-db=db \
	--enable-cgibindir=%{cgibindir} \
	%{?with_ssl:--enable-https} \
	%{?with_ispell:--with-ispell=/usr/bin/ispell} \
	--enable-mimetypes=/etc/mime.types \
	--enable-imagedir=%{imagedir} \
	--enable-imageurl=%{imageurl} \
	--with-cachedir=%{_localstatedir}/tmp \
	--with-cacheowner=%{cacheowner} \
	--with-mailer=/usr/sbin/sendmail \
	--with-piddir=/var/run
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{shared,shared.tmp} \
	$RPM_BUILD_ROOT/etc/{sysconfig,cron.hourly,rc.d/init.d,pam.d} \
%{?with_pl:$RPM_BUILD_ROOT%{_datadir}/sqwebmail/html/pl-pl}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install gpglib/webgpg $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.hourly/sqwebmail-cron-cleancache
install sqwebmail.init $RPM_BUILD_ROOT/etc/rc.d/init.d/sqwebmail

%if %{with pl}
tar zxf %{SOURCE3}
install sqwebmail-3.4.1-mgt.pl-beautifull_patch/html/pl-pl/* $RPM_BUILD_ROOT%{_datadir}/sqwebmail/html/pl-pl
%endif

rm $RPM_BUILD_ROOT%{_mandir}/man1/maildirmake.1
cp pcp/README.html pcp_README.html
echo net >$RPM_BUILD_ROOT%{_sysconfdir}/calendarmode

%if %{with ispell}
touch $RPM_BUILD_ROOT%{_datadir}/sqwebmail/html/en/ISPELLDICT
%endif

# make config file
./sysconftool $RPM_BUILD_ROOT%{_sysconfdir}/*.dist
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/*.dist

# delete man pages in conflict with courier-imap
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/deliverquota*
rm -f $RPM_BUILD_ROOT%{_libexecdir}/sqwebmaild.rc
# these conflict with courier-imap
rm -f $RPM_BUILD_ROOT%{_sbindir}/sharedindex{install,split}

# pam
cp sqwebmail/sqwebmail.pamconf $RPM_BUILD_ROOT/etc/pam.d/webmail
cp sqwebmail/sqwebmail.pamconf $RPM_BUILD_ROOT/etc/pam.d/calendar

# for apache
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -L %{_datadir}/sqwebmail/html/en ] || ln -fs en-us %{_datadir}/sqwebmail/html/en
/sbin/chkconfig --add sqwebmail
if [ -f /var/lock/subsys/sqwebmail ]; then
	/etc/rc.d/init.d/sqwebmail restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/sqwebmail start\" to start sqwebmail daemon."
fi

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del sqwebmail
	if [ -f /var/lock/subsys/sqwebmail ]; then
		/etc/rc.d/init.d/sqwebmail stop 1>&2
	fi
	[ ! -L %{_datadir}/sqwebmail/html/en ] || rm -f %{_datadir}/sqwebmail/html/en
fi

%post calendar
if [ -f /var/run/sqwebmaild.pid.pcp ]; then
	%{_sbindir}/courierlogger -pid=/var/run/sqwebmaild.pid.pcp -stop
	rm -f /var/run/sqwebmaild.pid.pcp
	%{_sbindir}/courierlogger -pid=/var/run/sqwebmaild.pid.pcp -start \
		%{_libexecdir}/sqwebmail/pcpd server
else
	if [ -f /var/lock/subsys/sqwebmail ]; then
		echo
		echo 'Type "/etc/rc.d/init.d/sqwebmail restart" to start sqwebmail with calendar'
		echo
	else
		echo
		echo 'Type "/etc/rc.d/init.d/sqwebmail start" to start sqwebmail with calendar'
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

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache >= 2.0.0
%webapp_register httpd %{_webapp}

%triggerun -- apache >= 2.0.0
%webapp_unregister httpd %{_webapp}

%triggerpostun -- %{name} < 5.0.4-1.1
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
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi
if [ "$apache_reload" ]; then
	/usr/sbin/webapp register apache %{_webapp}
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache reload 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS sqwebmail/BUGS INSTALL NEWS README sqwebmail/SECURITY sqwebmail/TODO gpglib/README.html
%doc sqwebmail/BUGS.html INSTALL.html README.html sqwebmail/SECURITY.html sqwebmail/TODO.html sqwebmail/ChangeLog
%doc maildir/README*.html gpglib/README.html
%attr(755,root,root) %{cgibindir}/sqwebmail

%attr(755,root,root) %{_sbindir}/webgpg

%dir %{_libexecdir}/sqwebmail
%attr(755,root,root) %{_libexecdir}/sqwebmail/deliverquota
%attr(755,root,root) %{_libexecdir}/sqwebmail/maildirmake
%attr(755,root,root) %{_libexecdir}/sqwebmail/makemime
%attr(755,root,root) %{_libexecdir}/sqwebmail/reformime
%attr(755,root,root) %{_libexecdir}/sqwebmail/sqwebmaild
%attr(2755, %{sqwebmailowner}, %{sqwebmailgroup}) %{_libexecdir}/sqwebmail/sqwebpasswd

%dir %{_sysconfdir}
%attr(755,daemon,daemon) %dir %{_sysconfdir}/shared
%attr(755,daemon,daemon) %dir %{_sysconfdir}/shared.tmp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ldapaddressbook
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sqwebmaild
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf

%dir %{_datadir}/sqwebmail
%dir %{_datadir}/sqwebmail/html
%dir %{_datadir}/sqwebmail/html/en-us
%{imagedir}
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/en-us/CHARSET
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/en-us/LANGUAGE
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/en-us/LANGUAGE_PREF
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/en-us/LOCALE
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/en-us/TIMEZONELIST
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/sqwebmail/html/en-us/ISPELLDICT
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/webmail
%{_datadir}/sqwebmail/html/en-us/*.html
%{_datadir}/sqwebmail/html/en-us/*.txt
%attr(755,root,root) %{_datadir}/sqwebmail/ldapsearch
%attr(755,root,root) %{_datadir}/sqwebmail/webgpg
%attr(755,root,root) %{_datadir}/sqwebmail/sendit.sh
%attr(755,bin,root) %{_datadir}/sqwebmail/cleancache.pl

%attr(754,root,root) /etc/rc.d/init.d/sqwebmail
%attr(755,root,root) /etc/cron.hourly/sqwebmail-cron-cleancache

%attr(771,root,daemon) %dir %{_localstatedir}
%attr(700,%{cacheowner},bin) %dir %{_localstatedir}/tmp

%files calendar
%defattr(644,root,root,755)
%doc pcp_README.html
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
