# TODO:
# - python module (make pymod, unset SONAME for python module)
#
Summary:	A library to make your web software pac (proxy auto-config) files intelligent
Summary(pl.UTF-8):	Biblioteka do obsługi plików pac (automatycznej konfiguracji proxy)
Name:		pacparser
Version:	1.3.0
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	http://pacparser.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	6dcfda10803913df38249fb39990dd87
#Source0Download: http://code.google.com/p/pacparser/downloads/list
Patch0:		%{name}-make.patch
Patch1:		%{name}-libdir.patch
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} -C src \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I/usr/include/js -DXP_UNIX" \
	LDFLAGS="%{rpmldflags} -ljs" \
	LIB=%{_lib}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIB=%{_lib}

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
