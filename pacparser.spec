Summary:	A library to make your web software pac (proxy auto-config) files intelligent
Summary(pl.UTF-8):	-
Name:		pacparser
Version:	1.0.8
Release:	0.1
License:	GPL v3
Group:		Libraries
Source0:	http://pacparser.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	3aec8fd4473a24698f7f4aefb0a79069
Patch0:		%{name}-include_path.patch
URL:		http://code.google.com/p/pacparser/
BuildRequires:	js-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pacparser is a library to parse proxy auto-config (PAC) files. Proxy
auto-config files are a vastly used proxy configuration method these
days. Web browsers can use a PAC file to determine which proxy server
to use or whether to go direct for a given URL. PAC files are written
in JavaScript and can be programmed to return different proxy methods
(e.g. "PROXY proxy1:port; DIRECT") depending upon URL, source IP
address, protocol, time of the day etc. PAC files introduce a lot of
possibilities. Look at the wikipedia link above to find out more about
them.

Needless to say, PAC files are now a widely accepted method for proxy
configuration management and companies all over are using them in
corporate environment. Almost all popular web browsers support PAC
files. The idea behind pacparser is to make it easy to add this PAC
file parsing capability to any program (C and python supported right
now). It comes as a shared C library and a python module which can be
used to make any C or python program PAC scripts intelligent. Some
very useful targets could be popular web software like wget, curl and
python-urllib.

%description -l pl.UTF-8

%package devel
Summary:	Header files for pacparser library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki pacparser
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for pacparser library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki pacparser.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I/usr/include/js -DXP_UNIX" \
	LDFLAGS="%{rpmldflags} -ljs"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %ghost %{_libdir}/libpacparser.so.1
%{_mandir}/man1/pactester.1*

%files devel
%defattr(644,root,root,755)
%{_mandir}/man3/pacparser*.3*
%{_libdir}/libpacparser.so
%{_includedir}/pacparser.h
