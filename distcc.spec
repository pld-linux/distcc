# TODO
# - unpackaged files:
#   /etc/default/distcc
#   /etc/distcc/clients.allow
#   /etc/distcc/commands.allow.sh
#   /etc/distcc/hosts
#   /usr/lib64/python2.6/site-packages/include_server-3.1-py2.6.egg-info
#
# Conditional build:
%bcond_without	gnome	# build without gnome(monitor) support
#
Summary:	Program to distribute compilation of C or C++
Summary(pl.UTF-8):	Program do rozdzielania kompilacji programów w C lub C++
Name:		distcc
Version:	3.1
Release:	0.1
License:	GPL
Group:		Development/Languages
Source0:	http://distcc.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	a1a9d3853df7133669fffec2a9aab9f3
Source1:	%{name}.inetd
Source2:	%{name}.init
Source3:	%{name}.sh
Source4:	%{name}.csh
Source5:	%{name}.config
Source6:	%{name}.logrotate
Patch0:		%{name}-user.patch
URL:		http://www.distcc.org/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
%{?with_gnome:BuildRequires:	libgnomeui-devel >= 2.0}
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	python-devel
BuildRequires:	python-devel-tools
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

sed -i -e 's#PKGDATADIR#"%{_pixmapsdir}"#g' src/mon-gnome.c

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--enable-rfc2553 \
	%{?with_gnome:--with-gnome}

%{__make} \
	WERROR_CFLAGS="" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig/rc-inetd,rc.d/init.d,profile.d,logrotate.d} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_var}/log}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/distccd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/distcc
install %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT/etc/profile.d
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/distccd
install %{SOURCE6} $RPM_BUILD_ROOT/etc/logrotate.d/distccd

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%if %{with gnome}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/distccmon-gnome.desktop \
	$RPM_BUILD_ROOT%{_desktopdir}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/distccmon-gnome-icon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}
%endif

touch $RPM_BUILD_ROOT%{_var}/log/distcc
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}


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
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/lsdistcc
%attr(755,root,root) %{_bindir}/pump
%{_mandir}/man?/%{name}.*
%{_mandir}/man1/pump.1*
%attr(755,root,root) /etc/profile.d/*sh

%files common
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/distccd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/distccd
%attr(755,root,root) %{_bindir}/%{name}d
%{_mandir}/man?/%{name}d.*
%attr(640,distcc,root) %ghost %{_var}/log/distcc

%files include_server
%defattr(644,root,root,755)
%{py_sitedir}/include_server
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
%{_mandir}/man1/distccmon-text.*

%if %{with gnome}
%files monitor-gnome
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/distccmon-gnome
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
%endif
