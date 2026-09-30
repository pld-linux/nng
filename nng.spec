# Conditional build:
%bcond_without	tests		# unit tests

Summary:	Light-weight brokerless messaging
Summary(pl.UTF-8):	Lekka biblioteka komunikatów bez pośrednika
Name:		nng
Version:	1.12.4
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/nanomsg/nng/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	da16997d0e92022248e4952eb9fc9d7f
Patch0:		install.patch
Patch1:		man-sections.patch
Patch2:		nngcat-tests-tmpdir.patch
URL:		https://nanomsg.github.io/nng/
BuildRequires:	cmake
BuildRequires:	mbedtls-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	ruby-asciidoctor

%description
nng (nanomsg next generation) is a socket library that provides
several common communication patterns. It aims to make the networking
layer fast, scalable, and easy to use. Implemented in C, it works on a
wide range of operating systems with no further dependencies.

The communication patterns, also called "scalability protocols", are
basic blocks for building distributed systems. By combining them you
can create a vast array of distributed applications.

%description -l pl.UTF-8
nng (nanomsg next generation) to biblioteka gniazd udostępniająca
kilka popularnych wzorców komunikacji. Jej celem jest zapewnienie
szybkiej, skalowalnej i łatwej w użyciu warstwy sieciowej. Jest
napisana w C i działa na wielu systemach operacyjnych bez dodatkowych
zależności.

Wzorce komunikacji, zwane też "protokołami skalowalności", są
podstawowymi elementami do budowy systemów rozproszonych. Łącząc je,
można tworzyć różnorodne aplikacje rozproszone.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains files needed to develop applications using
nanomsg, a socket library that provides several common communication
patterns.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki potrzebne do tworzenia aplikacji
wykorzystujących nng - bibliotekę gniazd udostępniającą kilka
popularnych wzorców komunikacji.

%package utils
Summary:	Command line interface for communicating with nng
Summary(pl.UTF-8):	Interfejs wiersza poleceń do komunikacji przez nng
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description utils
Includes nngcat, a simple utility for reading and writing to nanomsg
sockets and bindings, which can include local and remote connections.

%description utils -l pl.UTF-8
Ten pakiet zawiera nngcat - proste narzędzie do odczytu i zapisu
danych przez gniazda nanomsg, zarówno przy połączeniach lokalnych, jak
i zdalnych.

%prep
%setup -q

%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
%cmake -B build \
	-DBUILD_SHARED_LIBS=ON \
	-DNNG_ENABLE_TLS=ON \
	-DNNG_ENABLE_NNGCAT=ON \
	%{cmake_on_off tests NNG_TESTS} \
	-DNNG_ENABLE_DOC=ON

%{__make} -C build

%if %{with tests}
# ipc sockets and scratch files of the tests stay inside the build tree
export TMPDIR=$(pwd)/tests-tmp
install -d $TMPDIR
# talks to httpbin.org and other public servers
ctest_exclude='^nng\.httpclient$'
# getaddrinfo() with AI_ADDRCONFIG rejects even 127.0.0.1 when only loopback is configured
ctest_exclude="$ctest_exclude|^nng\.(tls|platform\.resolver_test|sp\.transport\.(tcp|tls|ws)\..*|supplemental\.wssfile_test)$"
# every test starts dozens of threads, parallel runs exhaust the task limit
ctest --test-dir build --output-on-failure -E "$ctest_exclude"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.adoc UKRAINE.adoc LICENSE.txt
%{_libdir}/libnng.so.*.*.*
%ghost %{_libdir}/libnng.so.1

%files devel
%defattr(644,root,root,755)
%{_docdir}/nng/
%{_includedir}/nng/
%{_libdir}/libnng.so
%{_libdir}/cmake/nng/
%{_mandir}/man3/*.3*
%{_mandir}/man5/*.5.*
%{_mandir}/man7/*.7.*

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nngcat
%{_mandir}/man1/nngcat.1*

