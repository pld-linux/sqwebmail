
%define _with_mysql     1
%define _with_ssl       1


Summary:	SqWebMail - Maildir Webmail CGI client
Summary(pl):	SqWebMail - Klient pocztowy CGI dla skrzynek Maildir
Name:		sqwebmail
Version:	3.5.0
Release:	0.2
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/courier/%{name}-%{version}.tar.bz2
Source1:	%{name}-cron-cleancache
Source2:	%{name}.init
Source3:        %{name}-3.4.1-mgt.pl-beautifull_patch.tgz
Patch0:		%{name}-authpam_patch
URL:		http://www.inter7.com/sqwebmail/
Requires(post,preun):	/sbin/chkconfig
Requires:	crondaemon
Requires:	expect
Requires:	gnupg >= 1.0.4
BuildRequires:	expect
BuildRequires:	gdbm-devel
BuildRequires:	gnupg >= 1.0.4
%{?_with_mysql:BuildRequires:     mysql-devel}
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	perl
BuildRequires:	postgresql-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define httpddir                /home/services/httpd
%define cgibindir               %{httpddir}/cgi-bin
%define imagedir                %{httpddir}/html/webmail
%define imageurl                /webmail

%define htmllibdir              /usr/share/sqwebmail
%define cachedir                /var/cache/sqwebmail

%define _prefix                 %{htmllibdir}
%define _sbindir		/usr/sbin
%define _bindir			/usr/bin
%define _mandir			/usr/man
%define _libexecdir             /usr/lib/sqwebmail
%define	_sysconfdir		/etc/sqwebmail

%define cacheowner              bin
%define sqwebmailowner          root
%define sqwebmailgroup          mail
%define sqwebmailperm           06555

%description
SqWebMail is a Webmail CGI for Maildir mailboxes.

%description(pl)
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
Ten pakiet zawiera pliki niezbêdne do uwierzytelniania poprzez LDAP.

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
Ten pakiet zawiera pliki niezbêdne do uwierzytelniania przy u¿yciu
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
Ten pakiet zawiera pliki niezbêdne do uwierzytelniania przy u¿yciu
tabeli w bazie PostgreSQL.

%prep
%setup -q
%patch0 -p1

%build

%configure --prefix=%{_prefix} \
           --sbindir=%{_sbindir} \
           --sysconfdir=%{_sysconfdir}/sqwebmail \
           --libexecdir=%{_libexecdir} \
           --mandir=%{_mandir} \
           --enable-cgibindir=%{cgibindir} \
%{?_with_mysql: --without-authvchkpw} \
%{?_with_mysql: --with-mysql} \
%{?_with_ssl: --enable-https} \
           --enable-imageurl=%{imagedir} \
           --with-cachedir=%{cachedir} \
           --enable-cgibindir=%{cgibindir} \
           --enable-imagedir=%{imagedir} \
           --enable-imageurl=%{imageurl} \
           --with-cacheowner=%{cacheowner}


%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{pam.d,rc.d/init.d,sysconfig,profile.d,cron.hourly,sqwebmail} \
           $RPM_BUILD_ROOT%{_libexecdir}/authlib \
           $RPM_BUILD_ROOT%{_sbindir} \
           $RPM_BUILD_ROOT%{_mandir}/{man1,man7,man8} \
           $RPM_BUILD_ROOT%{httpddir} \
	   $RPM_BUILD_ROOT%{htmllibdir}/pl-pl \
           $RPM_BUILD_ROOT%{cgibindir} \
           $RPM_BUILD_ROOT%{imagedir} \
           $RPM_BUILD_ROOT%{_prefix} \
           $RPM_BUILD_ROOT%{cachedir}


install -m 0444 sqwebmail/webmail.authpam $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/webmail
install -m 0444 sqwebmail/webmail.authpam $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/calendar

install authmodulelist $RPM_BUILD_ROOT%{_prefix}/authmodulelist
#install configlist $RPM_BUILD_ROOT%{htmllibdir}/configlist
install sysconftool $RPM_BUILD_ROOT%{_prefix}/sysconftool
install authlib/authdaemond $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond
install authlib/authdaemond.ldap $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.ldap
install authlib/authsystem.passwd $RPM_BUILD_ROOT%{_libexecdir}/authlib/authsystem.passwd
#install authlib/authdaemond.mysql $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.mysql
install authlib/authdaemond.plain $RPM_BUILD_ROOT%{_libexecdir}/authlib/authdaemond.plain
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/sqwebmail-cron-cleancache
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/sqwebmail

%{__make} install DESTDIR=$RPM_BUILD_ROOT

tar zxf %{SOURCE3}
install sqwebmail-3.4.1-mgt.pl-beautifull_patch/html/pl-pl/* $RPM_BUILD_ROOT%{htmllibdir}/pl-pl

cp pcp/README.html pcp_README.html

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -d %{htmllibdir}/html/en ] || ln -fs en-us %{htmllibdir}/html/en
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
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS sqwebmail/BUGS INSTALL INSTALL.vchkpw NEWS README sqwebmail/SECURITY sqwebmail/TODO gpglib/README.html
%doc sqwebmail/BUGS.html INSTALL.html NEWS.html README.html sqwebmail/SECURITY.html sqwebmail/TODO.html sqwebmail/ChangeLog pcp_README.html
%doc maildir/README*.html
%attr(%{sqwebmailperm}, %{sqwebmailowner}, %{sqwebmailgroup}) %{cgibindir}/sqwebmail

%{imagedir}
%{_prefix}

%attr(755,root,root) %{_sbindir}/*
%dir %{_libexecdir}/authlib
# note: too many files here (duplicated in subpackages)
%attr(755,root,root) %{_libexecdir}/authlib/*
%dir %{_libexecdir}
%dir %{_libexecdir}/sqwebmail
%attr(755,root,root) %{_libexecdir}/sqwebmail/*

%dir %{_sysconfdir}
%attr(644, root, root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/authdaemonrc.dist
%attr(644, root, root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/authmodulelist
%attr(644, root, root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sqwebmail/ldapaddressbook.dist
%attr(644, root, root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pam.d/*
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/*

%attr(755,root,root) /etc/rc.d/init.d/sqwebmail
%attr(755,root,root) /etc/cron.hourly/sqwebmail-cron-cleancache

%attr(700, %{cacheowner}, bin) %dir %{cachedir}

%{_mandir}/man?/*

%files ldap
%defattr(644,root,root,755)
%{_libexecdir}/authlib/authdaemond.ldap
%{_sysconfdir}/sqwebmail/authldaprc.dist


#%files mysql
#%defattr(644,root,root,755)
#%{_libexecdir}/authlib/authdaemond.mysql

%files pgsql
%defattr(644,root,root,755)
%{_libexecdir}/authlib/authdaemond.pgsql
%{_sysconfdir}/sqwebmail/authpgsqlrc.dist
