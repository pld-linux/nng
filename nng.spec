# Conditional build:
%bcond_with	tests		# build with tests

Summary:	Light-weight brokerless messaging
Summary(pl.UTF-8):	-
Name:		nng
Version:	1.11
Release:	0.1
License:	MIT
Group:		Libraries
Source0:	https://github.com/nanomsg/nng/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e901b96cbf0626076f2b05ffbc2012b8
Patch0:		install.patch
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

%package  devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains files needed to develop applications using
nanomsg, a socket library that provides several common communication
patterns.

%package utils
Summary:	Command line interface for communicating with nng
Requires:	%{name} = %{version}-%{release}

%description utils
Includes nngcat, a simple utility for reading and writing to nanomsg
sockets and bindings, which can include local and remote connections.

%prep
%setup -q

%patch -P0 -p1

%build
%cmake -B build \
	-DBUILD_SHARED_LIBS=ON \
	-DNNG_ENABLE_TLS=ON \
	-DNNG_ENABLE_NNGCAT=ON \
	-DNNG_TESTS=%{!?with_tests:OFF}%{?with_tests:ON} \
	-DNNG_ENABLE_DOC=ON

%{__make} -C build

%{?with_tests:%{__make} -C build test ARGS=--output-on-failure}

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
%{_libdir}/libnng.so.1*

%files devel
%defattr(644,root,root,755)
%{_docdir}/nng/
%{_includedir}/nng/
%{_libdir}/libnng.so
%{_libdir}/cmake/nng/
%{_mandir}/man3/*.3.*
%{_mandir}/man5/*.5.*
%{_mandir}/man7/*.7.*

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nngcat
%{_mandir}/man1/nngcat.1*

