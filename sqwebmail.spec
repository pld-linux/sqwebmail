Summary:	SqWebMail - Maildir Webmail CGI client.
Summary(pl): 	SqWebMail - Klient pocztyowy CGI.
Name: 		sqwebmail
Version: 	3.5.0
Release: 	0.1
License: 	GPL
Group: 		Applications/Mail
Source: 	http://download.sourceforge.net/courier/%{name}-%{version}.tar.bz2
Source1:	%{name}-cron-cleancache
Source2:	%{name}.init
Patch0:		%{name}-authpam_patch
Url: 		http://www.inter7.com/sqwebmail/
Requires: 	/sbin/chkconfig 
Requires: 	gnupg >= 1.0.4 
Requires: 	vixie-cron 
Requires: 	expect
BuildPreReq: 	rpm >= 4.0.2 
BuildPreReq: 	mawk
BuildPreReq: 	fileutils 
BuildPreReq: 	grep 
BuildPreReq: 	perl 
BuildPreReq: 	gdbm-devel 
BuildPreReq: 	gnupg >= 1.0.4 
BuildPreReq: 	expect 
BuildPreReq: 	pam-devel 
BuildPreReq: 	openldap-devel 
#BuildPreReq: 	mysql-devel 
BuildPreReq: 	postgresql-devel
BuildRoot: 	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%define httpddir                /home/httpd
%define cgibindir               %{httpddir}/cgi-bin
%define imagedir                %{httpddir}/html/webmail
%define imageurl                /webmail

%define htmllibdir              /usr/share/sqwebmail
%define cachedir                /var/cache/sqwebmail

%define _prefix                 %{htmllibdir}
%define _sbindir		/usr/sbin
%define _bindir			/usr/bin
%define _mandir			/usr/man
%define _libexecdir             /usr/libexec/sqwebmail

%define cacheowner              bin
%define sqwebmailowner          root
%define sqwebmailgroup          mail
%define sqwebmailperm           06555


%description
SqWebMail is a Webmail CGI for Maildir mailboxes.

%description(pl)
SqWebMail jest klientem pocztowym CGI, bazuj±cym na Maildira'ch

%package ldap
Summary: 	SqWebMail LDAP authentication driver.
Summary(pl): 	SqWebMail LDAP sterownik autoryzacji.
Group: 		Applications/Mail
Requires: 	sqwebmail = 3.5.0

%description ldap
This package contains the necessary files to allow SqWebMail to
authenticate from an LDAP directory.  Install this package if you need
the ability to use an LDAP directory for authentication.

%description(pl) ldap
Ten pakiet zawiera pliki niezbedne do autoryzacji poprz LDAP'a.
Zainstaluj go jezeli potrzebujesz wsparcia od strony LDAP'a.

%package mysql
Summary: 	SqWebMail MySQL authentication driver.
Summary(pl): 	SqWebMail MySQL sterownik autoryzacji.
Group: 		Applications/Mail
Requires: 	sqwebmail = 3.5.0

%description mysql
This package contains the necessary files to allow SqWebMail to
authenticate using a MySQL database table.  Install this package if you need
the ability to use a MySQL database table for authentication.

%description(pl) mysql
Ten pakiet zawiera pliki niezbedne do autoryzacji poprzez
baze MySQL.

%package 	pgsql
Summary: 	SqWebMail PostgreSQL authentication driver.
Summary(pl): 	SqWebMail PostgreSQL sterownik autoryzacji.
Group: 		Applications/Mail
Requires: 	sqwebmail = 3.5.0

%description pgsql
This package contains the necessary files to allow SqWebMail to
authenticate using a PostgreSQL database table.  Install this package if you
need the ability to use a PostgreSQL database table for authentication.

%description(pl) pgsql
Ten pakiet zawiera pliki niezbedne do autoryzacji poprzez
baze PostgreSQL.



%prep
%setup -q

%patch0 -p1

%configure --prefix=%{_prefix} \
	   --sbindir=%{_sbindir} \
	   --sysconfdir=%{_sysconfdir}/sqwebmail \
	   --libexecdir=%{_libexecdir} \
	   --mandir=%{_mandir} \
	   --enable-cgibindir=%{cgibindir} \
	   --without-authvchkpw \
	   --enable-imageurl=%{imagedir} \
	   --with-cachedir=%{cachedir} \
   	   --enable-cgibindir=%{cgibindir} \
	   --enable-imagedir=%{imagedir} \
	   --enable-imageurl=%{imageurl} \
	   --with-cacheowner=%{cacheowner} 

	
%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{pam.d,rc.d/init.d,sysconfig,profile.d,cron.hourly,sqwebmail} \
	   $RPM_BUILD_ROOT%{_libexecdir} \
	   $RPM_BUILD_ROOT%{_libexecdir}/authlib \
	   $RPM_BUILD_ROOT%{_sbindir} \
	   $RPM_BUILD_ROOT%{_mandir}/{man1,man7,man8} \
	   $RPM_BUILD_ROOT%{httpddir} \
	   $RPM_BUILD_ROOT%{cgibindir} \
	   $RPM_BUILD_ROOT%{imagedir} \
	   $RPM_BUILD_ROOT%{htmllibdir} \
	   $RPM_BUILD_ROOT%{cachedir} 

install -m 0444 sqwebmail/webmail.authpam $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/webmail
install -m 0444 sqwebmail/webmail.authpam $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/calendar

install authmodulelist $RPM_BUILD_ROOT%{htmllibdir}/authmodulelist
#install configlist $RPM_BUILD_ROOT%{htmllibdir}/configlist
install sysconftool $RPM_BUILD_ROOT%{htmllibdir}/sysconftool
install authlib/authdaemond $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond
install authlib/authdaemond.ldap $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.ldap
install authlib/authsystem.passwd $RPM_BUILD_ROOT%{_libexecdir}/authlib/authsystem.passwd
#install authlib/authdaemond.mysql $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.mysql
install authlib/authdaemond.plain $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.plain
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/sqwebmail-cron-cleancache
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/sqwebmail

%{__make} install-strip DESTDIR=$RPM_BUILD_ROOT


cp pcp/README.html pcp_README.html

%post

[ -d %{htmllibdir}/html/en ] || ln -fs en-us %{htmllibdir}/html/en
/sbin/chkconfig --add sqwebmail

%preun

/sbin/chkconfig --del sqwebmail

if [ -f /var/lock/subsys/sqwbmail ]; then
	/etc/rc.d/init.d/sqwebmail stop
fi

%postun
[ -d %{htmllibdir}/html/en ] || rm -f %{htmllibdir}/html/en

%files
%defattr(644, root, root,755)
%attr(%{sqwebmailperm}, %{sqwebmailowner}, %{sqwebmailgroup}) %{cgibindir}/sqwebmail

%{imagedir}/*
%{htmllibdir}/*

%attr(755, root, root) %{_sbindir}/*
%attr(755, root, root) %{_libexecdir}/authlib/*
%attr(755, root, root) %{_libexecdir}/sqwebmail/*

%attr(644, root, root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/*
%attr(644, root, root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pam.d/*

%attr(755, root, root) %{_sysconfdir}/rc.d/init.d/sqwebmail
%attr(755, root, root) %{_sysconfdir}/cron.hourly/sqwebmail-cron-cleancache

%attr(700, %{cacheowner}, bin) %dir %{cachedir}

%{_mandir}/man?/*

%doc AUTHORS sqwebmail/BUGS INSTALL INSTALL.vchkpw NEWS README sqwebmail/SECURITY sqwebmail/TODO gpglib/README.html
%doc sqwebmail/BUGS.html INSTALL.html NEWS.html README.html sqwebmail/SECURITY.html sqwebmail/TODO.html sqwebmail/ChangeLog pcp_README.html
%doc maildir/README*.html


%files ldap 
%defattr(644, root, bin,755)
%{_libexecdir}/authlib/authdaemond.ldap

#%files mysql
#%defattr(-, root, bin)
##%attr(644, root, bin) %{_libexecdir}/authlib/authdaemond.mysql

%files pgsql
%defattr(644, root, bin,755)
%{_libexecdir}/authlib/authdaemond.pgsql

%clean
rm -rf $RPM_BUILD_ROOT
