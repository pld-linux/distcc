#
# Conditional build:
%bcond_without	gnome	# build without gnome(monitor) support
#
Summary:	Program to distribute compilation of C or C++
Summary(pl):	Program do rozdzielania kompilacji program�w w C lub C++
Name:		distcc
Group:		Development/Languages
Version:	2.18
Release:	1
License:	GPL
Source0:	http://distcc.samba.org/ftp/distcc/%{name}-%{version}.tar.bz2
# Source0-md5:	a55b547d4ff62d8500e290b82671db50
# Source0-size:	339939
Source1:	%{name}.inetd
Source2:	%{name}.init
Source3:	%{name}.sh
Source4:	%{name}.csh
Source5:	%{name}.config
Source6:	%{name}.logrotate
Patch0:		%{name}-user.patch
URL:		http://distcc.samba.org/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
%{?with_gnome:BuildRequires:	libgnomeui-devel >= 2.0}
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

%description -l pl
distcc jest programem pozwalaj�cym na dystrybucj� kompilacji C lub C++
na kilka maszyn w sieci. distcc powinien zawsze generowa� takie same
rezultaty jak lokalna kompilacja, jest prosty w instalacji i u�yciu
oraz bardzo cz�sto dwa lub wi�cej razy szybszy ni� lokalna kompilacja.

%package common
Summary:	Common files for inetd and standalone versions of distcc
Summary(pl):	Pliki wsp�lne dla wersji inetd i standalone distcc
Group:		Daemons
Requires:	gcc
Requires:	gcc-c++
Requires(pre): 	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Obsoletes:	distcc < 2.1-2

%description common
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

%description common -l pl
distcc jest programem pozwalaj�cym na dystrybucj� kompilacji C lub C++
na kilka maszyn w sieci. distcc powinien zawsze generowa� takie same
rezultaty jak lokalna kompilacja, jest prosty w instalacji i u�yciu
oraz bardzo cz�sto dwa lub wi�cej razy szybszy ni� lokalna kompilacja.

%package inetd
Summary:	inetd configs for distcc
Summary(pl):	Pliki konfiguracyjne do u�ycia distcc poprzez inetd
Group:		Daemons
PreReq:		%{name}-common = %{version}-%{release}
PreReq:		rc-inetd
Obsoletes:	distcc < 2.1-2

%description inetd
distcc configs for running from inetd.

%description inetd -l pl
Pliki konfiguracyjna distcc do startowania demona poprzez inetd.

%package standalone
Summary:	Standalone daemon configs for distcc
Summary(pl):	Pliki konfiguracyjne do startowania distcc w trybie standalone
Group:		Daemons
PreReq:		%{name}-common = %{version}-%{release}
PreReq:		rc-scripts
Obsoletes:	distcc < 2.1-2

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
%patch0 -p1

sed -i -e 's#PKGDATADIR#"%{_pixmapsdir}"#g' src/mon-gnome.c

%build
cp -f /usr/share/automake/config.* .
%{__autoconf}
%{__autoheader}
%configure \
	--enable-rfc2553 \
	%{?with_gnome:--with-gnome} 

%{__make}

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

%if %{with gnome}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/distccmon-gnome.desktop \
	$RPM_BUILD_ROOT%{_desktopdir}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/distccmon-gnome-icon.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}
%endif

touch $RPM_BUILD_ROOT%{_var}/log/distcc

%clean
rm -rf $RPM_BUILD_ROOT

%pre common
if [ -n "`getgid distcc`" ]; then
        if [ "`getgid distcc`" != "137" ]; then
                echo "Error: group distcc doesn't have gid=137. Correct this before installing distccd." 1>&2
                exit 1
        fi
else
        /usr/sbin/groupadd -g 137 -r -f distcc
fi
if [ -n "`/bin/id -u distcc 2>/dev/null`" ]; then
	if [ "`/bin/id -u distcc`" != "137" ]; then
		echo "Error: user distcc doesn't have uid=137. Correct this before installing distccd server." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 137 -d /tmp -s /bin/false -c "distcc user" -g distcc distcc 1>&2
fi

%postun common
if [ "$1" = "0" ]; then
        %userremove distcc
        %groupremove distcc
fi

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
%attr(755,root,root) /etc/profile.d/*sh

%files common
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/distccd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/distccd
%attr(755,root,root) %{_bindir}/%{name}d
%{_mandir}/man?/%{name}d.*
%attr(640,distcc,root) %ghost %{_var}/log/distcc

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/distccd

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
