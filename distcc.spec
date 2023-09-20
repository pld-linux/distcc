# TODO
# - unpackaged files:
#   /etc/distcc/clients.allow
#   /etc/distcc/commands.allow.sh
#   /etc/distcc/hosts
#
# Conditional build:
%bcond_without	gtk	# distccmon-gnome tool (monitor-gnome package)
%bcond_with	gnome	# GNOME libraries support in distccmon-gnome (not ported to GNOME 3)

Summary:	Program to distribute compilation of C or C++
Summary(pl.UTF-8):	Program do rozdzielania kompilacji programów w C lub C++
Name:		distcc
Version:	3.4
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	https://github.com/distcc/distcc/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	00523fd05f4cd9dd968e4e0ec09d774d
Source1:	%{name}.inetd
Source2:	%{name}.init
Source3:	%{name}.sh
Source4:	%{name}.csh
Source5:	%{name}.config
Source6:	%{name}.logrotate
Patch0:		%{name}-user.patch
Patch1:		%{name}-python.patch
URL:		http://www.distcc.org/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
# libiberty
BuildRequires:	binutils-devel
%{?with_gtk:BuildRequires:	gtk+3-devel}
%{?with_gnome:BuildRequires:	libgnome-devel >= 3.0}
%{?with_gnome:BuildRequires:	libgnomeui-devel >= 3.0}
%{?with_gnome:BuildRequires:	pango-devel}
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	python3-devel >= 1:3.1
BuildRequires:	python3-devel-tools >= 1:3.1
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

%description -l pl.UTF-8
distcc jest programem pozwalającym na dystrybucję kompilacji C lub C++
na kilka maszyn w sieci. distcc powinien zawsze generować takie same
rezultaty jak lokalna kompilacja, jest prosty w instalacji i użyciu
oraz bardzo często dwa lub więcej razy szybszy niż lokalna kompilacja.

%package common
Summary:	Common files for inetd and standalone versions of distcc
Summary(pl.UTF-8):	Pliki wspólne dla wersji inetd i standalone distcc
Group:		Daemons
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Suggests:	gcc
Suggests:	gcc-c++
Provides:	group(distcc)
Provides:	user(distcc)
Obsoletes:	distcc < 2.1-2

%description common
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

%description common -l pl.UTF-8
distcc jest programem pozwalającym na dystrybucję kompilacji C lub C++
na kilka maszyn w sieci. distcc powinien zawsze generować takie same
rezultaty jak lokalna kompilacja, jest prosty w instalacji i użyciu
oraz bardzo często dwa lub więcej razy szybszy niż lokalna kompilacja.

%package include_server
Summary:	Conservative approximation of include dependencies for C/C++
Summary(pl.UTF-8):	Konserwatywna aproksymacja zależności nagłówków dla C/C++
Group:		Daemons

%description include_server
include_server.py starts an include server process. This process
answers queries from distcc(1) clients about what files to include in
C/C++ compilations. The include_server.py command itself terminates as
soon as the include server has been spawned.

%description include_server -l pl.UTF-8
include_server.py wywołuje proces serwera include. Proces ten
odpowiada na zapytania klientów distcc(1) dotyczące plików, które
należy dołączyć na etapie kompilacji C/C++. Polecenie
incluse_server.py kończy działanie jak tylko wywołany zostanie proces
serwera.

%package inetd
Summary:	inetd configs for distcc
Summary(pl.UTF-8):	Pliki konfiguracyjne do użycia distcc poprzez inetd
Group:		Daemons
Requires:	%{name}-common = %{version}-%{release}
Requires:	rc-inetd
Obsoletes:	distcc < 2.1-2

%description inetd
distcc configs for running from inetd.

%description inetd -l pl.UTF-8
Pliki konfiguracyjna distcc do startowania demona poprzez inetd.

%package standalone
Summary:	Standalone daemon configs for distcc
Summary(pl.UTF-8):	Pliki konfiguracyjne do startowania distcc w trybie standalone
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	rc-scripts
Obsoletes:	distcc < 2.1-2

%description standalone
distcc configs for running as a standalone daemon.

%description standalone -l pl.UTF-8
Pliki konfiguracyjne distcc do startowania demona w trybie standalone.

%package monitor
Summary:	Monitor for distcc
Summary(pl.UTF-8):	Monitor dla distcc
Group:		Applications

%description monitor
Monitor for distcc.

%description monitor -l pl.UTF-8
Monitor dla distcc.

%package monitor-gnome
Summary:	GTK+ monitor for distcc
Summary(pl.UTF-8):	Monitor GTK+ dla distcc
Group:		X11/Applications

%description monitor-gnome
GTK+ monitor for distcc.

%description monitor-gnome -l pl.UTF-8
Monitor GTK+ dla distcc.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{__sed} -i -e 's#PKGDATADIR#"%{_pixmapsdir}"#g' src/mon-gnome.c

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
	update-distcc-symlinks.py

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--enable-rfc2553 \
	%{?with_gnome:--with-gnome} \
	%{?with_gtk:--with-gtk}

%{__make} \
	WERROR_CFLAGS=""
#	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig/rc-inetd,rc.d/init.d,profile.d,logrotate.d} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_var}/log}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/distccd
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/distcc
cp -p %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT/etc/profile.d
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/default/distcc
cp -p %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/distccd
cp -p %{SOURCE6} $RPM_BUILD_ROOT/etc/logrotate.d/distccd

touch $RPM_BUILD_ROOT%{_var}/log/distcc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre common
%groupadd -P %{name}-common -g 137 distcc
%useradd -P %{name}-common -u 137 -d /tmp -s /bin/false -c "distcc user" -g distcc distcc

%postun common
if [ "$1" = "0" ]; then
	%userremove distcc
	%groupremove distcc
fi

%post inetd
%service -q rc-inetd reload

%postun inetd
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%post standalone
/sbin/chkconfig --add distcc
%service distcc restart "distcc daemon"

%preun standalone
if [ "$1" = "0" ]; then
	%service distcc stop
	/sbin/chkconfig --del distcc
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README *.txt
%attr(755,root,root) %{_bindir}/distcc
%attr(755,root,root) %{_bindir}/lsdistcc
%attr(755,root,root) %{_bindir}/pump
%attr(755,root,root) %{_sbindir}/update-distcc-symlinks
%{_mandir}/man1/distcc.1*
%{_mandir}/man1/pump.1*
%{_mandir}/man1/lsdistcc.1*
%attr(755,root,root) /etc/profile.d/distcc.csh
%attr(755,root,root) /etc/profile.d/distcc.sh

%files common
%defattr(644,root,root,755)
%dir /etc/distcc
/etc/distcc/clients.allow
/etc/distcc/commands.allow.sh
/etc/distcc/hosts
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/distccd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/distccd
%attr(755,root,root) %{_bindir}/distccd
%{_mandir}/man1/distccd.1*
%attr(640,distcc,root) %ghost %{_var}/log/distcc

%files include_server
%defattr(644,root,root,755)
%{py3_sitedir}/include_server
%{py3_sitedir}/include_server-%{version}-py*.egg-info
%{_mandir}/man1/include_server.1*

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/distccd

%files standalone
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/distcc

%files monitor
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/distccmon-text
%{_mandir}/man1/distccmon-text.1*

%if %{with gtk}
%files monitor-gnome
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/distccmon-gnome
%{_desktopdir}/distccmon-gnome.desktop
%{_pixmapsdir}/distccmon-gnome.png
%endif
