Summary:	Program to distribute compilation of C or C++
Summary(pl):	Program do rozdzielania kompilacji programów w C lub C++
Name:		distcc
Group:		Development/Languages
Version:	1.2.3
Release:	2
License:	GPL
URL:		http://distcc.samba.org
Source0:	http://distcc.samba.org/ftp/distcc/%{name}-%{version}.tar.bz2
Source1:	%{name}.inetd
Source2:	%{name}.sh
Source3:	%{name}.csh
Patch0:		%{name}-user.patch
Requires:	gcc
Requires:	gcc-c++
Requires:	inetdaemon
BuildRequires:	popt-devel
Prereq:         /sbin/chkconfig
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

%prep
%setup -q

%patch -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd \
	   $RPM_BUILD_ROOT/etc/profile.d

%{makeinstall}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/distccd
install %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT/etc/profile.d

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
if [ -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd reload 1>&2
else
        echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
if [ -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd reload
fi

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README linuxdoc/html/*
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %{_mandir}/man?/*
%attr(640,root,root) /etc/sysconfig/rc-inetd/distccd
%attr(644,root,root) /etc/profile.d/*sh
%{_infodir}/distcc*
