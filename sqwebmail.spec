Summary:	SqWebMail - Maildir Webmail CGI client
Summary(pl):	SqWebMail - Klient pocztowy CGI dla skrzynek Maildir
Name:		sqwebmail
Version:	3.5.0
Release:	0.5
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/courier/%{name}-%{version}.tar.bz2
Source1:	%{name}-cron-cleancache
Source2:	%{name}.init
Source3:	%{name}-3.4.1-mgt.pl-beautifull_patch.tgz
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
%{!?_without_ispell:Requires: ispell}
BuildRequires:	expect
BuildRequires:	gdbm-devel
BuildRequires:	gnupg >= 1.0.4
%{!?_without_mysql:BuildRequires:	mysql-devel}
%{!?_without_ldap:BuildRequires:	openldap-devel}
%{!?_without_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	pam-devel
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

%package ldap
Summary:	SqWebMail LDAP authentication driver
Summary(pl):	Sterownik uwierzytelnienia LDAP dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description ldap
This package contains the necessary files to allow SqWebMail to
authenticate from an LDAP directory. Install this package if you need
the ability to use an LDAP directory for authentication.

%description ldap -l pl
Ten pakiet zawiera pliki niezb�dne do uwierzytelniania poprzez LDAP.

%package mysql
Summary:	SqWebMail MySQL authentication driver
Summary(pl):	Sterownik uwierzytelnienia MySQL dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description mysql
This package contains the necessary files to allow SqWebMail to
authenticate using a MySQL database table. Install this package if you
need the ability to use a MySQL database table for authentication.

%description mysql -l pl
Ten pakiet zawiera pliki niezb�dne do uwierzytelniania przy u�yciu
tabeli w bazie MySQL.

%package 	pgsql
Summary:	SqWebMail PostgreSQL authentication driver
Summary(pl):	Sterownik uwierzytelnienia PostgreSQL dla SqWebMaila
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description pgsql
This package contains the necessary files to allow SqWebMail to
authenticate using a PostgreSQL database table. Install this package
if you need the ability to use a PostgreSQL database table for
authentication.

%description pgsql -l pl
Ten pakiet zawiera pliki niezb�dne do uwierzytelniania przy u�yciu
tabeli w bazie PostgreSQL.

%package        userdb
Summary:        SqWebMail userdb authentication driver
Summary(pl):    Sterownik uwierzytelnienia userdb dla SqWebMaila
Group:          Applications/Mail
Obsoletes:	courier-imap-userdb
Requires:       %{name} = %{version}

%description userdb
This package contains the necessary files to allow SqWebMail to
authenticate using a userdb file.

%description userdb -l pl
Ten pakiet zawiera pliki niezb�dne do uwierzytelniania przy u�yciu
pliku userdb.

%package        calendar
Summary:        SqWebMail calendar
Summary(pl):    Kalendarz dla SqWebMaila
Group:          Applications/Mail
Requires:       %{name} = %{version}

%description calendar
Calendar

%description calendar -l pl
Kalendarz


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure --sysconfdir=%{_sysconfdir}/sqwebmail \
	   --libexecdir=%{_libexecdir} \
	   --enable-cgibindir=%{cgibindir} \
%{!?_without_ldap: --with-authldap} \
%{!?_without_userdb: --with-authuserdb} \
%{!?_without_userdb: --with-userdb=%{_sysconfdir}/sqwebmail/userdb } \
%{!?_without_pgsql: --with-authpgsql} \
%{!?_without_mysql: --without-authvchkpw} \
%{!?_without_mysql: --enable-mysql=y} \
%{!?_without_mysql: --with-mysql-include=/usr/include/mysql} \
%{!?_without_mysql: --with-mysql-libs=/usr/lib} \
%{!?_without_ssl: --enable-https} \
%{!?_without_ispell:	--with-ispell=/usr/bin/ispell} \
	   --enable-mimetypes=/etc/mime.types \
	   --enable-imageurl=%{imagedir} \
	   --with-cachedir=%{cachedir} \
	   --enable-imagedir=%{imagedir} \
	   --enable-imageurl=%{imageurl} \
	   --with-cacheowner=%{cacheowner} \
	   --with-authdaemonvar=%{authdaemonvar} \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sqwebmail \
	   $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,sysconfig,cron.hourly,sqwebmail} \
           $RPM_BUILD_ROOT%{_libexecdir}/authlib \
           $RPM_BUILD_ROOT%{_sbindir} \
           $RPM_BUILD_ROOT%{_mandir}/{man1,man7,man8} \
           $RPM_BUILD_ROOT%{httpddir} \
	   $RPM_BUILD_ROOT%{htmllibdir}/pl-pl \
           $RPM_BUILD_ROOT%{cgibindir} \
           $RPM_BUILD_ROOT%{imagedir} \
           $RPM_BUILD_ROOT%{_prefix} \
           $RPM_BUILD_ROOT%{cachedir} \
	   $RPM_BUILD_ROOT%{authdaemonvar}


install -m 0444 sqwebmail/webmail.authpam $RPM_BUILD_ROOT/etc/pam.d/webmail
install -m 0444 sqwebmail/webmail.authpam $RPM_BUILD_ROOT/etc/pam.d/calendar

install authmodulelist $RPM_BUILD_ROOT%{_prefix}/authmodulelist
install sysconftool $RPM_BUILD_ROOT%{_prefix}/sysconftool
install authlib/authdaemond $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond


%if 0%{!?_without_ldap:1}
install authlib/authdaemond.ldap $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.ldap
%endif

%if 0%{!?_without_mysql:1}
install authlib/authdaemond.mysql $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.mysql
%endif

%if 0%{!?_without_pgsql:1}
install authlib/authdaemond.pgsql $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.pgsql
%endif

%if 0%{!?_without_userdb:1}
install authlib/authdaemond.pgsql $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.userdb
%endif

install authlib/authdaemond.plain $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.plain
install authlib/authsystem.passwd $RPM_BUILD_ROOT%{_libexecdir}/authlib/authsystem.passwd
install pcpd $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.hourly/sqwebmail-cron-cleancache
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/sqwebmail

%{__make} install DESTDIR=$RPM_BUILD_ROOT

tar zxf %{SOURCE3}
install sqwebmail-3.4.1-mgt.pl-beautifull_patch/html/pl-pl/* $RPM_BUILD_ROOT%{htmllibdir}/pl-pl

rm $RPM_BUILD_ROOT%{_mandir}/man1/maildirmake.1

cp pcp/README.html pcp_README.html

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -L %{htmllibdir}/html/en ] || ln -fs en-us %{htmllibdir}/html/en
[ -L %{htmllibdir}/html/pl ] || ln -fs pl-pl %{htmllibdir}/pl
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
	[ ! -L %{htmllibdir}/html/en ] || rm -f %{htmllibdir}/html/en
	[ ! -L %{htmllibdir}/html/pl ] || rm -f %{htmllibdir}/pl
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS sqwebmail/BUGS INSTALL INSTALL.vchkpw NEWS README sqwebmail/SECURITY sqwebmail/TODO gpglib/README.html
%doc sqwebmail/BUGS.html INSTALL.html NEWS.html README.html sqwebmail/SECURITY.html sqwebmail/TODO.html sqwebmail/ChangeLog
%doc maildir/README*.html
%attr(%{sqwebmailperm}, %{sqwebmailowner}, %{sqwebmailgroup}) %{cgibindir}/sqwebmail

%{imagedir}
%{_prefix}

#%attr(755,root,root) %{_sbindir}/*
%dir %{_libexecdir}/authlib
%attr(755,root,root) %{_libexecdir}/authlib/authdaemon
%attr(755,root,root) %{_libexecdir}/authlib/authdaemon.passwd
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.plain
%attr(755,root,root) %{_libexecdir}/authlib/authsystem.passwd
%dir %{_libexecdir}
%dir %{_libexecdir}/sqwebmail
%attr(755,root,root) %{_libexecdir}/sqwebmail/*

%dir %{_sysconfdir}/sqwebmail
%attr(644, root, root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/authdaemonrc.dist
%attr(644, root, root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/authmodulelist
%attr(644, root, root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/ldapaddressbook.dist
%attr(644, root, root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/nodsn
%attr(644, root, root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/*

%attr(755,root,root) /etc/rc.d/init.d/sqwebmail
%attr(755,root,root) /etc/cron.hourly/sqwebmail-cron-cleancache

%attr(700, %{cacheowner}, bin) %dir %{cachedir}
%dir %{authdaemonvar}
%{_mandir}/man7/authlib.*
%{_mandir}/man7/authcram.*
%{_mandir}/man7/authdaemon.*
%{_mandir}/man7/authdaemond.*
%{_mandir}/man7/authpam.*
%{_mandir}/man7/authpwd.*
%{_mandir}/man7/authshadow.*
%{_mandir}/man8/deliverquota.*

%if 0%{!?_without_ldap:1}
%files ldap
%defattr(644,root,root,755)
%doc authlib/authldap.schema
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.ldap
%{_sysconfdir}/sqwebmail/authldaprc.dist
%{_mandir}/man7/authldap.*
%endif

%if 0%{!?_without_mysql:1}
%files mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.mysql
%{_sysconfdir}/sqwebmail/authmysqlrc.dist
%{_mandir}/man7/authmysql.*
%endif

%if 0%{!?_without_pgsql:1}
%files pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.pgsql
%{_sysconfdir}/sqwebmail/authpgsqlrc.dist
%endif

%if 0%{!?_without_userdb:1}
%files userdb
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.userdb
%{_sysconfdir}/sqwebmail/authpgsqlrc.dist
%attr(755,root,root) %{_sbindir}/makeuserdb
%attr(755,root,root) %{_sbindir}/pw2userdb
%attr(755,root,root) %{_sbindir}/userdb
%attr(755,root,root) %{_sbindir}/userdbpw
%attr(755,root,root) %{_sbindir}/vchkpw2userdb
%{_mandir}/man7/authuserdb.7
%{_mandir}/man8/makeuserdb.8.gz
%{_mandir}/man8/pw2userdb.8
%{_mandir}/man8/userdb.8.gz
%{_mandir}/man8/userdbpw.8.gz
%{_mandir}/man8/vchkpw2userdb.8
%endif

%files calendar
%defattr(644,root,root,755)
%doc pcp_README.html
%{_sbindir}/pcpd
