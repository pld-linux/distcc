#
# Conditional build:
# _without_gtk	build without gtk2(monitor) support
#
Summary:	Program to distribute compilation of C or C++
Summary(pl):	Program do rozdzielania kompilacji programów w C lub C++
Name:		distcc
Group:		Development/Languages
Version:	2.10.1
Release:	1
License:	GPL
URL:		http://distcc.samba.org/
Source0:	http://distcc.samba.org/ftp/distcc/%{name}-%{version}.tar.bz2
# Source0-md5:	7eeccb1a68d52c02bd96864e532e0870
Source1:	%{name}.inetd
Source2:	%{name}.init
Source3:	%{name}.sh
Source4:	%{name}.csh
Source5:	%{name}.config
Patch0:		%{name}-user.patch
%{!?_without_gtk:BuildRequires:	gtk+2-devel >= 2.0}
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
Summary:	standalone daemon configs for distcc
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

%prep
%setup -q
%patch -p1

%build
%configure \
	%{!?_without_gtk:--enable-gnome}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd \
	   $RPM_BUILD_ROOT/etc/rc.d/init.d \
	   $RPM_BUILD_ROOT/etc/profile.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/distccd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/distcc
install %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT/etc/profile.d
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/distccd

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

%files common
%defattr(644,root,root,755)
%doc AUTHORS NEWS README *.txt
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/distccd
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %{_mandir}/man?/*
%attr(644,root,root) /etc/profile.d/*sh

%files inetd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/distccd

%files standalone
%attr(755,root,root) /etc/rc.d/init.d/distcc
