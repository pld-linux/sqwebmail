Summary:	SqWebMail - Maildir Webmail CGI client
Summary(pl):	SqWebMail - Klient pocztowy CGI dla skrzynek Maildir
Name:		sqwebmail
Version:	3.5.3
Release:	0.9
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	3eadaf5ad1cb942666da9a34e7b7109d
Source1:	%{name}-cron-cleancache
Source2:	%{name}.init
Source3:	%{name}-3.4.1-mgt.pl-beautifull_patch.tgz
# Source3-md5:	702b4075c7e8b6ae71c895a8bb803aa9
Patch0:		%{name}-authpam_patch
Patch1:		%{name}-mysqlauth.patch
Patch2:		%{name}-prowizorka.patch
URL:		http://www.inter7.com/sqwebmail/
Requires(post,preun):	/sbin/chkconfig
Requires:	crondaemon
Requires:	expect
Requires:	gnupg >= 1.0.4
Requires:	apache
Requires:	mailcap
Requires:	perl
%{!?_without_ispell:Requires:	ispell}
%{!?_without_ssl:Requires:	apache-mod_ssl}
BuildRequires:	expect
BuildRequires:	gdbm-devel
BuildRequires:	gnupg >= 1.0.4
%{!?_without_mysql:BuildRequires:	mysql-devel}
%{!?_without_ldap:BuildRequires:	openldap-devel}
%{!?_without_pgsql:BuildRequires:	postgresql-devel}
%{!?_without_pam:BuildRequires:		pam-devel}
BuildRequires:	perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define httpddir                /home/services/httpd
%define cgibindir               %{httpddir}/cgi-bin
%define imagedir                %{httpddir}/html/webmail
%define imageurl                /webmail

%define htmllibdir              /usr/share/sqwebmail
%define cachedir                /var/cache/sqwebmail
%define authdaemonvar		/var/cache/authdaemonvar

%define _prefix                 %{htmllibdir}
%define _sbindir		/usr/sbin
%define _bindir			/usr/bin
%define _mandir			/usr/share/man
%define _libexecdir             /usr/lib/sqwebmail
%define	_sysconfdir		/etc

%define cacheowner              bin
%define sqwebmailowner          root
%define sqwebmailgroup          mail
%define sqwebmailperm           06555

%description
SqWebMail is a Webmail CGI for Maildir mailboxes.

%description -l pl
SqWebMail jest klientem pocztowym CGI dla skrzynek Maildir.

%package auth-ldap
Summary:	SqWebMail LDAP authentication driver
Summary(pl):	Sterownik uwierzytelnienia LDAP dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description auth-ldap
This package contains the necessary files to allow SqWebMail to
authenticate from an LDAP directory. Install this package if you need
the ability to use an LDAP directory for authentication.

%description auth-ldap -l pl
Ten pakiet zawiera pliki niezbêdne do uwierzytelniania poprzez LDAP.

%package auth-mysql
Summary:	SqWebMail MySQL authentication driver
Summary(pl):	Sterownik uwierzytelnienia MySQL dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description auth-mysql
This package contains the necessary files to allow SqWebMail to
authenticate using a MySQL database table. Install this package if you
need the ability to use a MySQL database table for authentication.

%description auth-mysql -l pl
Ten pakiet zawiera pliki niezbêdne do uwierzytelniania przy u¿yciu
tabeli w bazie MySQL.

%package auth-pgsql
Summary:	SqWebMail PostgreSQL authentication driver
Summary(pl):	Sterownik uwierzytelnienia PostgreSQL dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description auth-pgsql
This package contains the necessary files to allow SqWebMail to
authenticate using a PostgreSQL database table. Install this package
if you need the ability to use a PostgreSQL database table for
authentication.

%description auth-pgsql -l pl
Ten pakiet zawiera pliki niezbêdne do uwierzytelniania przy u¿yciu
tabeli w bazie PostgreSQL.

%package auth-userdb
Summary:	SqWebMail userdb authentication driver
Summary(pl):	Sterownik uwierzytelnienia userdb dla SqWebMaila
Group:		Applications/Mail
Obsoletes:	courier-imap-userdb
Requires:	%{name} = %{version}

%description auth-userdb
This package contains the necessary files to allow SqWebMail to
authenticate using a userdb file.

%description auth-userdb -l pl
Ten pakiet zawiera pliki niezbêdne do uwierzytelniania przy u¿yciu
pliku userdb.

%package auth-pam
Summary:	SqWebMail pam authentication driver
Summary(pl):	Sterownik uwierzytelnienia pam dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description auth-pam
This package contains the necessary files to allow SqWebMail to
authenticate using a pam.

%description auth-pam -l pl
Ten pakiet zawiera pliki niezbêdne do uwierzytelniania przy u¿yciu
biblioteki pam.

%package auth-pwd
Summary:	SqWebMail pwd authentication driver
Summary(pl):	Sterownik uwierzytelnienia pwd dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description auth-pwd
This package contains the necessary files to allow SqWebMail to
authenticates from the /etc/passwd file.

%description auth-pwd -l pl
Ten pakiet zawiera pliki niezbêdne do uwierzytelniania przy u¿yciu
pliku /etc/passwd.

%package auth-shadow
Summary:	SqWebMail shadow authentication driver
Summary(pl):	Sterownik uwierzytelnienia shadow dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description auth-shadow
This package contains the necessary files to allow SqWebMail to
authenticates from the /etc/shadow file.

%description auth-shadow -l pl
Ten pakiet zawiera pliki niezbêdne do uwierzytelniania przy u¿yciu
pliku /etc/shadow.

%package auth-cram
Summary:	SqWebMail cram authentication driver
Summary(pl):	Sterownik uwierzytelnienia cram dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description auth-cram
This package contains the necessary files to allow SqWebMail to
authenticate using cram mechanism.

%description auth-cram -l pl
Ten pakiet zawiera pliki niezbêdne do uwierzytelniania przy u¿yciu
mechanizmu cram.

%package calendar
Summary:	SqWebMail calendar
Summary(pl):	Kalendarz dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description calendar
SqWebMail Calendar.

%description calendar -l pl
Kalendarz SqWebMaila.

%package pl_html
Summary:	SqWebMail - Polish translation
Summary(pl):	Sqwebmail - polska wersja interfejsu
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description pl_html
Polish translation.

%description pl_html -l pl
Polskie t³umaczenie interfejsu.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure \
	--sysconfdir=%{_sysconfdir}/sqwebmail \
	--libexecdir=%{_libexecdir} \
	--enable-cgibindir=%{cgibindir} \
	%{!?_without_ldap:--with-authldap} \
	%{!?_without_pam:--with-authpam} \
	%{!?_without_pwd:--with-authpwd} \
	%{!?_without_pwd:--with-authshadow} \
	%{!?_without_cram:--with-authcram} \
	%{!?_without_userdb:--with-authuserdb} \
	%{!?_without_userdb:--with-userdb=%{_sysconfdir}/sqwebmail/userdb } \
	%{!?_without_pgsql:--with-authpgsql} \
	%{!?_without_mysql:--without-authvchkpw} \
	%{!?_without_mysql:--enable-mysql=y} \
	%{!?_without_mysql:--with-mysql-include=/usr/include/mysql} \
	%{!?_without_mysql:--with-mysql-libs=/usr/lib} \
	%{!?_without_ssl:--enable-https} \
	%{!?_without_ispell:--with-ispell=/usr/bin/ispell} \
	--enable-mimetypes=/etc/mime.types \
	--enable-imageurl=%{imagedir} \
	--with-cachedir=%{cachedir} \
	--enable-imagedir=%{imagedir} \
	--enable-imageurl=%{imageurl} \
	--with-cacheowner=%{cacheowner} \
	--with-authdaemonvar=%{authdaemonvar}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail \
	   $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,sysconfig,cron.hourly,sqwebmail} \
           $RPM_BUILD_ROOT%{_libexecdir}/authlib \
           $RPM_BUILD_ROOT%{_sbindir} \
           $RPM_BUILD_ROOT%{_mandir}/{man1,man7,man8} \
           $RPM_BUILD_ROOT%{httpddir} \
	   $RPM_BUILD_ROOT%{htmllibdir}/html/pl-pl \
           $RPM_BUILD_ROOT%{cgibindir} \
           $RPM_BUILD_ROOT%{imagedir} \
           $RPM_BUILD_ROOT%{_prefix} \
           $RPM_BUILD_ROOT%{cachedir} \
	   $RPM_BUILD_ROOT%{authdaemonvar}

%{__make} install DESTDIR=$RPM_BUILD_ROOT


install authmodulelist $RPM_BUILD_ROOT%{_prefix}/authmodulelist
install sysconftool $RPM_BUILD_ROOT%{_prefix}/sysconftool
install authlib/authdaemond $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond


%if 0%{!?_without_ldap:1}
install authlib/authdaemond.ldap $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.ldap
mv $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/authldaprc.dist $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/authldaprc
%endif

%if 0%{!?_without_mysql:1}
install authlib/authdaemond.mysql $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.mysql
mv $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/authmysqlrc.dist $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/authmysqlrc
%endif

%if 0%{!?_without_pgsql:1}
install authlib/authdaemond.pgsql $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.pgsql
mv $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/authpgsqlrc.dist $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/authpgsqlrc
%endif

%if 0%{!?_without_userdb:1}
install authlib/authuserdb $RPM_BUILD_ROOT%{_libexecdir}/authlib/authuserdb
%endif

%if 0%{!?_without_pam:1}
install authlib/authpam $RPM_BUILD_ROOT%{_libexecdir}/authlib/authpam
install -m 0444 sqwebmail/webmail.authpam $RPM_BUILD_ROOT/etc/pam.d/webmail
install -m 0444 sqwebmail/webmail.authpam $RPM_BUILD_ROOT/etc/pam.d/calendar
%endif

%if 0%{!?_without_pwd:1}
install authlib/authsystem.passwd $RPM_BUILD_ROOT%{_libexecdir}/authlib/authsystem.passwd
%endif

%if 0%{!?_without_shadow:1}
install authlib/authshadow $RPM_BUILD_ROOT%{_libexecdir}/authlib/authshadow
%endif

%if 0%{!?_without_cram:1}
install authlib/authcram $RPM_BUILD_ROOT%{_libexecdir}/authlib/authcram
%endif

install authlib/authdaemond.plain $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.plain
install pcpd $RPM_BUILD_ROOT%{_sbindir}
install gpglib/webgpg $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.hourly/sqwebmail-cron-cleancache
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/sqwebmail


tar zxf %{SOURCE3}
install sqwebmail-3.4.1-mgt.pl-beautifull_patch/html/pl-pl/* $RPM_BUILD_ROOT%{htmllibdir}/html/pl-pl

rm $RPM_BUILD_ROOT%{_mandir}/man1/maildirmake.1
mv $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/authdaemonrc.dist $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/authdaemonrc
mv $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/ldapaddressbook.dist $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail/ldapaddressbook
cp pcp/README.html pcp_README.html

%if 0%{!?_without_ispell:1}
touch $RPM_BUILD_ROOT%{htmllibdir}/html/en/ISPELLDICT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -L %{htmllibdir}/html/en ] || ln -fs en-us %{htmllibdir}/html/en
/sbin/chkconfig --add sqwebmail
if [ -f /var/lock/subsys/sqwebmail ]; then
	/etc/rc.d/init.d/sqwebmail restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/sqwebmail start\" to start sqwebmail daemon."
fi

%post pl_html
[ -L %{htmllibdir}/html/pl ] || ln -fs pl-pl %{htmllibdir}/html/pl
echo "echo 'pl-pl' > /usr/share/sqwebmail/html/en/LANGUAGE"

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del sqwebmail
	if [ -f /var/lock/subsys/sqwebmail ]; then
		/etc/rc.d/init.d/sqwebmail stop 1>&2
	fi
	[ ! -L %{htmllibdir}/html/en ] || rm -f %{htmllibdir}/html/en
fi

%preun pl_html
[ ! -L %{htmllibdir}/html/pl ] || rm -f %{htmllibdir}/pl


%files
%defattr(644,root,root,755)
%doc AUTHORS sqwebmail/BUGS INSTALL INSTALL.vchkpw NEWS README sqwebmail/SECURITY sqwebmail/TODO gpglib/README.html
%doc sqwebmail/BUGS.html INSTALL.html NEWS.html README.html sqwebmail/SECURITY.html sqwebmail/TODO.html sqwebmail/ChangeLog
%doc maildir/README*.html
%attr(%{sqwebmailperm}, %{sqwebmailowner}, %{sqwebmailgroup}) %{cgibindir}/sqwebmail

%{imagedir}
%{_prefix}
%attr(755,root,root) %{_sbindir}/webgpg

%dir %{_libexecdir}
%dir %{_libexecdir}/authlib
%attr(755,root,root) %{_libexecdir}/authlib/authdaemon
%attr(755,root,root) %{_libexecdir}/authlib/authdaemon.passwd
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.plain
%attr(755,root,root) %{_libexecdir}/authlib/authsystem.passwd
%dir %{_libexecdir}/sqwebmail
%attr(755,root,root) %{_libexecdir}/sqwebmail/*

%dir %{_sysconfdir}/sqwebmail
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/authdaemonrc
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/authmodulelist
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/ldapaddressbook
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/nodsn
%dir %{htmllibdir}
%dir %{htmllibdir}/html
%dir %{htmllibdir}/html/en
%config(noreplace) %verify(not size mtime md5) %{htmllibdir}/html/en/CHARSET
%config(noreplace) %verify(not size mtime md5) %{htmllibdir}/html/en/LANGUAGE
%config(noreplace) %verify(not size mtime md5) %{htmllibdir}/html/en/LANGUAGE_PREF
%config(noreplace) %verify(not size mtime md5) %{htmllibdir}/html/en/LOCALE
%config(noreplace) %verify(not size mtime md5) %{htmllibdir}/html/en/TIMEZONELIST
%config(noreplace) %verify(not size mtime md5) %{htmllibdir}/html/en/ISPELLDICT
%config(noreplace) %verify(not size mtime md5) /etc/pam.d/*

%attr(754,root,root) /etc/rc.d/init.d/sqwebmail
%attr(755,root,root) /etc/cron.hourly/sqwebmail-cron-cleancache

%attr(700, %{cacheowner}, bin) %dir %{cachedir}
%dir %{authdaemonvar}
%{_mandir}/man7/authlib.*
%{_mandir}/man7/authdaemon.*
%{_mandir}/man7/authdaemond.*
%{_mandir}/man8/deliverquota.*

%if 0%{!?_without_ldap:1}
%files auth-ldap
%defattr(644,root,root,755)
%doc authlib/authldap.schema
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.ldap
%{_sysconfdir}/sqwebmail/authldaprc
%{_mandir}/man7/authldap.*
%endif

%if 0%{!?_without_mysql:1}
%files auth-mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.mysql
%{_sysconfdir}/sqwebmail/authmysqlrc
%{_mandir}/man7/authmysql.*
%endif

%if 0%{!?_without_pgsql:1}
%files auth-pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.pgsql
%{_sysconfdir}/sqwebmail/authpgsqlrc
%endif

%if 0%{!?_without_userdb:1}
%files auth-userdb
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/authlib/authuserdb
%attr(755,root,root) %{_sbindir}/makeuserdb
%attr(755,root,root) %{_sbindir}/pw2userdb
%attr(755,root,root) %{_sbindir}/userdb
%attr(755,root,root) %{_sbindir}/userdbpw
%attr(755,root,root) %{_sbindir}/vchkpw2userdb
%{_mandir}/man7/authuserdb.7*
%{_mandir}/man8/makeuserdb.8*
%{_mandir}/man8/pw2userdb.8*
%{_mandir}/man8/userdb.8*
%{_mandir}/man8/userdbpw.8*
%{_mandir}/man8/vchkpw2userdb.8*
%endif

%if 0%{!?_without_pam:1}
%files auth-pam
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/authlib/authpam
%{_mandir}/man7/authpam.*
%endif

%if 0%{!?_without_pwd:1}
%files auth-pwd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/authlib/authdaemon.passwd
%{_mandir}/man7/authpwd.*
%endif

%if 0%{!?_without_shadow:1}
%files auth-shadow
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/authlib/authshadow
%{_mandir}/man7/authshadow.*
%endif

%if 0%{!?_without_cram:1}
%files auth-cram
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/authlib/authcram
%{_mandir}/man7/authcram.*
%endif

%files calendar
%defattr(644,root,root,755)
%doc pcp_README.html
%{_sbindir}/pcpd

%files pl_html
%defattr(644,root,root,755)
%{htmllibdir}/pl-pl
%config(noreplace) %verify(not size mtime md5) %{htmllibdir}/html/pl-pl/CHARSET
%config(noreplace) %verify(not size mtime md5) %{htmllibdir}/html/pl-pl/LANGUAGE
%config(noreplace) %verify(not size mtime md5) %{htmllibdir}/html/pl-pl/LANGUAGE_PREF
%config(noreplace) %verify(not size mtime md5) %{htmllibdir}/html/pl-pl/LOCALE
%config(noreplace) %verify(not size mtime md5) %{htmllibdir}/html/pl-pl/TIMEZONELIST
%config(noreplace) %verify(not size mtime md5) %{htmllibdir}/html/pl-pl/ISPELLDICT
%{htmllibdir}/html/pl-pl/*.html
