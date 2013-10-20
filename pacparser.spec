#
# Conditional build:
%bcond_without	python	# Python module
#
Summary:	A library to make your web software pac (proxy auto-config) files intelligent
Summary(pl.UTF-8):	Biblioteka do obsługi plików pac (automatycznej konfiguracji proxy)
Name:		pacparser
Version:	1.3.1
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	http://pacparser.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	97010ef3c18f81f8734e3cc3d6f92619
#Source0Download: http://code.google.com/p/pacparser/downloads/list
Patch0:		%{name}-make.patch
Patch1:		%{name}-libdir.patch
Patch2:		%{name}-python.patch
URL:		http://code.google.com/p/pacparser/
BuildRequires:	js-devel >= 1.7.0
BuildRequires:	js-devel < 1.8.5
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pacparser is a library to parse proxy auto-config (PAC) files. Proxy
auto-config files are a vastly used proxy configuration method these
days. Web browsers can use a PAC file to determine which proxy server
to use or whether to go direct for a given URL. PAC files are written
in JavaScript and can be programmed to return different proxy methods
(e.g. "PROXY proxy1:port; DIRECT") depending upon URL, source IP
address, protocol, time of the day etc. PAC files introduce a lot of
possibilities.

Needless to say, PAC files are now a widely accepted method for proxy
configuration management and companies all over are using them in
corporate environment. Almost all popular web browsers support PAC
files. The idea behind pacparser is to make it easy to add this PAC
file parsing capability to any program (C and Python supported right
now). Some very useful targets could be popular web software like
wget, curl and python-urllib.

%description -l pl.UTF-8
pacparser to biblioteka do analizy plików automatycznej konfiguracji
proxy PAC (proxy auto-config). Pliki te są obecnie szeroko stosowaną
metodą do konfiguracji proxy. Przeglądarki potrafią użyć pliku PAC do
określenia, którego serwera proxy mają użyć lub jak połączyć się
bezpośrednio z danym URL-em. Pliki PAC są pisane w JavaScripcie i mogą
zwracać różne metody proxy (np. "PROXY proxy1:port; DIRECT") w
zależności od URL-a, adresu źródłowego IP, protokołu, pory dnia itp.
Pliki PAC wprowadzają wiele możliwości.

Nie trzeba mówić, że pliki PAC są teraz szeroko akceptowaną metodą
zarządzania konfiguracją proxy, a firmy używają ich w swoich
wewnętrznych środowiskach. Prawie wszystkie popularne przeglądarki WWW
obsługują pliki PAC. Ideą stojącą za biblioteką pacparser jest
ułatwienie dodawania obsługi PAC do dowolnego programu (obecnie
obsługiwane są języki C i Python). Przydatnymi zastosowaniami mogłyby
być popularne programy do stron WWW, takie jak wget, curl czy
python-urllib.

%package devel
Summary:	Header files for pacparser library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki pacparser
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for pacparser library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki pacparser.

%package -n python-pacparser
Summary:	Python interface for pacparser library
Summary(pl.UTF-8):	Interfejs Pythona do biblioteki pacparser
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-pacparser
Python interface for pacparser library.

%description -n python-pacparser -l pl.UTF-8
Interfejs Pythona do biblioteki pacparser.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%undos src/pymod/setup.py
%patch2 -p1

%build
%{__make} -C src \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I/usr/include/js -DXP_UNIX" \
	LDFLAGS="%{rpmldflags} -ljs" \
	LIB=%{_lib}

%if %{with python}
cd src/pymod
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags} -L$(pwd)/.." \
%{__python} setup.py build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIB=%{_lib}

%if %{with python}
cd src/pymod
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/pactester
%attr(755,root,root) %{_libdir}/libpacparser.so.1
%{_mandir}/man1/pactester.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpacparser.so
%{_includedir}/pacparser.h
%{_mandir}/man3/pacparser*.3*

%if %{with python}
%files -n python-pacparser
%defattr(644,root,root,755)
%dir %{py_sitedir}/pacparser
%attr(755,root,root) %{py_sitedir}/pacparser/_pacparser.so
%{py_sitedir}/pacparser/__init__.py[co]
%{py_sitedir}/pacparser-1-py*.egg-info
%endif
