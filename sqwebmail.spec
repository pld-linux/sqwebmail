#
# TODO
#	- tests
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
Version:	5.0.1
Release:	0.5
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	43bdf4521e8512411da5dad53395ca68
Source1:	%{name}-cron-cleancache
Source2:	%{name}.init
%{?with_pl:Source3:	%{name}-3.4.1-mgt.pl-beautifull_patch.tgz}
Patch0:		%{name}-authpam_patch
Patch1:		%{name}-prowizorka.patch
Patch2:		%{name}-maildir.patch
Patch3:		%{name}-init.patch
URL:		http://www.courier-mta.org/sqwebmail/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	courier-authlib-devel
BuildRequires:	db-devel
BuildRequires:	expect
BuildRequires:	fam-devel
BuildRequires:	gnupg >= 1.0.4
# perhaps only because of test sources written in C, but with ".C" extension(?)
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	perl-base
BuildRequires:	procps
BuildRequires:	sysconftool
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	crondaemon
Requires:	expect
Requires:	gnupg >= 1.0.4
Requires:	apache
Requires:	mailcap
%{?with_ispell:Requires:	ispell}
%{?with_ssl:Requires:	apache-mod_ssl}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_libexecdir		/usr/%{_lib}
%define	_localstatedir		/var/spool/sqwebmail

%define	httpddir		/home/services/httpd
%define	cgibindir		%{httpddir}/cgi-bin
%define	imagedir		%{_datadir}/sqwebmail/images
%define	imageurl		/webmail
%define	_apache1dir		/etc/apache
%define	_apache2dir		/etc/httpd

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

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--with-db=db \
	--sysconfdir=%{_sysconfdir}/sqwebmail \
	--libexecdir=%{_libexecdir} \
	--localstatedir=%{_localstatedir} \
	--enable-cgibindir=%{cgibindir} \
	%{?with_ssl:--enable-https} \
	%{?with_ispell:--with-ispell=/usr/bin/ispell} \
	--enable-mimetypes=/etc/mime.types \
	--enable-imagedir=%{imagedir} \
	--enable-imageurl=%{imageurl} \
	--with-cachedir=%{_localstatedir}/tmp \
	--with-cacheowner=%{cacheowner} \
	--with-mailer=%{_sbindir}/sendmail
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{sqwebmail/{shared,shared.tmp},pam.d} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,cron.hourly,rc.d/init.d,httpd} \
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
echo net >$RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/calendarmode

%if %{with ispell}
touch $RPM_BUILD_ROOT%{_datadir}/sqwebmail/html/en/ISPELLDICT
%endif

# make config file
./sysconftool $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/*.dist
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/*.dist

# delete man pages in conflict with courier-imap
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/deliverquota*
rm -f $RPM_BUILD_ROOT%{_libexecdir}/sqwebmaild.rc

# pam
cp sqwebmail/sqwebmail.pamconf $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/webmail

# for apache
echo "Alias /webmail %{imagedir}" >apache-%{name}.conf
install apache-%{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/apache-%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
# apache1
if [ -d %{_apache1dir}/conf.d ]; then
	ln -sf %{_sysconfdir}/sqwebmail/apache-%{name}.conf %{_apache1dir}/conf.d/99_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi
# apache2
if [ -d %{_apache2dir}/httpd.conf ]; then
	ln -sf %{_sysconfdir}/sqwebmail/apache-%{name}.conf %{_apache2dir}/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

[ -L %{_datadir}/sqwebmail/html/en ] || ln -fs en-us %{_datadir}/sqwebmail/html/en
/sbin/chkconfig --add sqwebmail
if [ -f /var/lock/subsys/sqwebmail ]; then
	/etc/rc.d/init.d/sqwebmail restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/sqwebmail start\" to start sqwebmail daemon."
fi

%preun
if [ "$1" = "0" ]; then
	# apache1
	if [ -d %{_apache1dir}/conf.d ]; then
		rm -f %{_apache1dir}/conf.d/99_%{name}.conf
		if [ -f /var/lock/subsys/apache ]; then
			/etc/rc.d/init.d/apache restart 1>&2
		fi
	fi
	# apache2
	if [ -d %{_apache2dir}/httpd.conf ]; then
		rm -f %{_apache2dir}/httpd.conf/99_%{name}.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/etc/rc.d/init.d/httpd restart 1>&2
		fi
	fi

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
		echo Type "/etc/rc.d/init.d/sqwebmail restart" to start sqwebmail with calendar
		echo
	else
		echo
		echo Type "/etc/rc.d/init.d/sqwebmail start" to start sqwebmail with calendar
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
echo "echo 'pl-pl' > /usr/share/sqwebmail/html/en/LANGUAGE"

%preun pl_html
[ ! -L %{_datadir}/sqwebmail/html/pl ] || rm -f %{_datadir}/sqwebmail/html/pl

%files
%defattr(644,root,root,755)
%doc AUTHORS sqwebmail/BUGS INSTALL INSTALL.vchkpw NEWS README sqwebmail/SECURITY sqwebmail/TODO gpglib/README.html
%doc sqwebmail/BUGS.html INSTALL.html README.html sqwebmail/SECURITY.html sqwebmail/TODO.html sqwebmail/ChangeLog
%doc maildir/README*.html gpglib/README.html
%attr(%{sqwebmailperm}, %{sqwebmailowner}, %{sqwebmailgroup}) %{cgibindir}/sqwebmail

%attr(755,root,root) %{_sbindir}/webgpg
%attr(755,root,root) %{_sbindir}/sharedindexinstall
%attr(755,root,root) %{_sbindir}/sharedindexsplit

%dir %{_libexecdir}/sqwebmail
%attr(755,root,root) %{_libexecdir}/sqwebmail/deliverquota
%attr(755,root,root) %{_libexecdir}/sqwebmail/maildirmake
%attr(755,root,root) %{_libexecdir}/sqwebmail/makemime
%attr(755,root,root) %{_libexecdir}/sqwebmail/reformime
%attr(755,root,root) %{_libexecdir}/sqwebmail/sqwebmaild
%attr(2755, %{sqwebmailowner}, %{sqwebmailgroup}) %{_libexecdir}/sqwebmail/sqwebpasswd

%dir %{_sysconfdir}/sqwebmail
%attr(755,daemon,daemon) %dir %{_sysconfdir}/sqwebmail/shared
%attr(755,daemon,daemon) %dir %{_sysconfdir}/sqwebmail/shared.tmp
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/ldapaddressbook
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/sqwebmaild
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/apache-%{name}.conf
%dir %{_datadir}/sqwebmail
%dir %{_datadir}/sqwebmail/html
%dir %{_datadir}/sqwebmail/html/en-us
%{imagedir}
%config(noreplace) %verify(not size mtime md5) %{_datadir}/sqwebmail/html/en-us/CHARSET
%config(noreplace) %verify(not size mtime md5) %{_datadir}/sqwebmail/html/en-us/LANGUAGE
%config(noreplace) %verify(not size mtime md5) %{_datadir}/sqwebmail/html/en-us/LANGUAGE_PREF
%config(noreplace) %verify(not size mtime md5) %{_datadir}/sqwebmail/html/en-us/LOCALE
%config(noreplace) %verify(not size mtime md5) %{_datadir}/sqwebmail/html/en-us/TIMEZONELIST
%config(noreplace) %verify(not size mtime md5) %{_datadir}/sqwebmail/html/en-us/ISPELLDICT
%config(noreplace) %verify(not size mtime md5) /etc/pam.d/*
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
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/calendarmode
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
%config(noreplace) %verify(not size mtime md5) %{_datadir}/sqwebmail/html/pl-pl/CHARSET
%config(noreplace) %verify(not size mtime md5) %{_datadir}/sqwebmail/html/pl-pl/LANGUAGE
%config(noreplace) %verify(not size mtime md5) %{_datadir}/sqwebmail/html/pl-pl/LANGUAGE_PREF
%config(noreplace) %verify(not size mtime md5) %{_datadir}/sqwebmail/html/pl-pl/LOCALE
%config(noreplace) %verify(not size mtime md5) %{_datadir}/sqwebmail/html/pl-pl/TIMEZONELIST
%config(noreplace) %verify(not size mtime md5) %{_datadir}/sqwebmail/html/pl-pl/ISPELLDICT
%endif
