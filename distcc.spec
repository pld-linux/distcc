#
# Conditional build:
%bcond_with	gnome	# build without gnome(monitor) support
#
Summary:	Program to distribute compilation of C or C++
Summary(pl):	Program do rozdzielania kompilacji programów w C lub C++
Name:		distcc
Group:		Development/Languages
Version:	2.11.2
Release:	1
License:	GPL
Source0:	http://distcc.samba.org/ftp/distcc/%{name}-%{version}.tar.bz2
# Source0-md5:	034bc9c36bd5c3d9c26241600510927b
Source1:	%{name}.inetd
Source2:	%{name}.init
Source3:	%{name}.sh
Source4:	%{name}.csh
Source5:	%{name}.config
Source6:	%{name}.logrotate
Patch0:		%{name}-user.patch
URL:		http://distcc.samba.org/
BuildRequires:	autoconf
%{?with_gtk:BuildRequires:	libgnome-devel >= 2.0}
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

%description -l pl
distcc jest programem pozwalaj±cym na dystrybucjê kompilacji C lub C++
na kilka maszyn w sieci. distcc powinien zawsze generowaæ takie same
rezultaty jak lokalna kompilacja, jest prosty w instalacji i u¿yciu
oraz bardzo czêsto dwa lub wiêcej razy szybszy ni¿ lokalna kompilacja.

%package common
Summary:	Common files for inetd and standalone versions of distcc
Summary(pl):	Pliki wspólne dla wersji inetd i standalone distcc
Group:		Daemons
Requires:	gcc
Requires:	gcc-c++
Obsoletes:	%{name} < %{name}-2.1-2

%description common
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

%description common -l pl
distcc jest programem pozwalaj±cym na dystrybucjê kompilacji C lub C++
na kilka maszyn w sieci. distcc powinien zawsze generowaæ takie same
rezultaty jak lokalna kompilacja, jest prosty w instalacji i u¿yciu
oraz bardzo czêsto dwa lub wiêcej razy szybszy ni¿ lokalna kompilacja.

%package inetd
Summary:	inetd configs for distcc
Summary(pl):	Pliki konfiguracyjne do u¿ycia distcc poprzez inetd
Group:		Daemons
PreReq:		%{name}-common = %{version}
PreReq:		rc-inetd
Obsoletes:	%{name} < %{name}-2.1-2

%description inetd
distcc configs for running from inetd.

%description inetd -l pl
Pliki konfiguracyjna distcc do startowania demona poprzez inetd.

%package standalone
Summary:	Standalone daemon configs for distcc
Summary(pl):	Pliki konfiguracyjne do startowania distcc w trybie standalone
Group:		Daemons
PreReq:		%{name}-common = %{version}
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Obsoletes:	%{name} < %{name}-2.1-2

%description standalone
distcc configs for running as a standalone daemon.

%description standalone -l pl
Pliki konfiguracyjne distcc do startowania demona w trybie
standalone.

%package monitor
Summary:        Monitor for distcc
Summary(pl):    Monitor dla distcc
Group:          Applications

%description monitor
Monitor for distcc.

%description monitor -l pl
Monitor dla distcc.

%package monitor-gnome
Summary:        gtk monitor for distcc
Summary(pl):    Monitor gtk dla distcc
Group:          X11/Applications

%description monitor-gnome
gtk monitor for distcc.

%description monitor-gnome -l pl
Monitor gtk dla distcc.

%prep
%setup -q
%patch -p1

%build
%{__autoconf}
%{__autoheader}
%configure \
	%{?with_gnome:--with-gnome}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig/rc-inetd,rc.d/init.d,profile.d,logrotate.d} \
	$RPM_BUILD_ROOT%{_applnkdir}/Network/Misc $RPM_BUILD_ROOT%{_pixmapsdir} \
	$RPM_BUILD_ROOT%{_var}/log

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/distccd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/distcc
install %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT/etc/profile.d
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/distccd
install %{SOURCE6} $RPM_BUILD_ROOT/etc/logrotate.d/distccd

%if %{with gnome}
mv $RPM_BUILD_ROOT%{_datadir}/distccmon-gnome.desktop \
	$RPM_BUILD_ROOT%{_applnkdir}/Network/Misc
mv $RPM_BUILD_ROOT%{_datadir}/distccmon-gnome-icon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}
%endif

touch $RPM_BUILD_ROOT%{_var}/log/distcc

%clean
rm -rf $RPM_BUILD_ROOT

%post inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%post standalone
/sbin/chkconfig --add distcc
if [ -f /var/lock/subsys/distccd ]; then
	/etc/rc.d/init.d/distcc restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/distcc start\" to start distcc daemon."
fi

%preun standalone
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/distccd ]; then
		/etc/rc.d/init.d/distcc stop 1>&2
	fi
	/sbin/chkconfig --del distcc
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README *.txt
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man?/%{name}.*
/etc/profile.d/*sh

%files common
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/distccd
%attr(640,root,root) %ghost %{_var}/log/distcc
%attr(640,root,root) /etc/logrotate.d/distccd
%attr(755,root,root) %{_bindir}/%{name}d
%{_mandir}/man?/%{name}d.*

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/distccd

%files standalone
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/distcc

%files monitor
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/distccmon-text
%if %{with gnome}
%attr(755,root,root) %{_bindir}/distccmon-gnome
%{_applnkdir}/Network/Misc/*.desktop
%{_pixmapsdir}/*
%endif
