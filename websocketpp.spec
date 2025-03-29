#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	C++ WebSocket Protocol Library
Summary(pl.UTF-8):	Biblioteka C++ do obsługi protokołu WebSocket
Name:		websocketpp
Version:	0.8.2
Release:	2
License:	BSD
Group:		Development/Libraries
#Source0Download: https://github.com/zaphoyd/websocketpp/releases
Source0:	https://github.com/zaphoyd/websocketpp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	261e977d69fdcb8fdaacb46b7c9e2258
Source1:	websocketpp.pc
Patch0:		%{name}-cmake_noarch.patch
Patch1:		%{name}-cmake-configversion-compatibility.patch
Patch2:		%{name}-tests.patch
Patch3:		boost-1.87.patch
Patch4:		%{name}-cmake-boost.patch
URL:		https://www.zaphoyd.com/websocketpp/
BuildRequires:	boost-devel >= 1.39
BuildRequires:	cmake >= 2.8.8
BuildRequires:	libstdc++-devel >= 6:4.7
# for tests
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WebSocket++ is an open source (BSD license) header only C++ library
that implements RFC6455 The WebSocket Protocol. It allows integrating
WebSocket client and server functionality into C++ programs. It uses
interchangeable network transport modules including one based on C++
iostreams and one based on Boost Asio.

%description -l pl.UTF-8
WebSocket++ to mająca otwarte źródła (na licencji BSD), składająca się
z samych nagłówków biblioteka C++ będąca implementacją protokołu
WebSocket (RFC6455). Pozwala na integrowanie funkcjonalności klienta i
serwera WebSocket w programach w C++. Wykorzystuje wymienne moduły
transportu sieciowego, w tym jeden oparty na iostreams z C++ i jeden
oparty o Boost Asio.

%package devel
Summary:	C++ WebSocket Protocol Library
Summary(pl.UTF-8):	Biblioteka C++ do obsługi protokołu WebSocket
Group:		Development/Libraries
Requires:	boost-devel >= 1.39
Requires:	libstdc++-devel >= 6:4.7

%description devel
WebSocket++ is an open source (BSD license) header only C++ library
that implements RFC6455 The WebSocket Protocol. It allows integrating
WebSocket client and server functionality into C++ programs. It uses
interchangeable network transport modules including one based on C++
iostreams and one based on Boost Asio.

%description devel -l pl.UTF-8
WebSocket++ to mająca otwarte źródła (na licencji BSD), składająca się
z samych nagłówków biblioteka C++ będąca implementacją protokołu
WebSocket (RFC6455). Pozwala na integrowanie funkcjonalności klienta i
serwera WebSocket w programach w C++. Wykorzystuje wymienne moduły
transportu sieciowego, w tym jeden oparty na iostreams z C++ i jeden
oparty o Boost Asio.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1

%build
install -d build
cd build
%cmake .. \
	%{?with_tests:-DBUILD_TESTS:BOOL=ON}

%{__make}

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_npkgconfigdir}
%{__sed} -e 's/@version@/%{version}/' %{SOURCE1} >$RPM_BUILD_ROOT%{_npkgconfigdir}/websocketpp.pc

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc COPYING changelog.md readme.md roadmap.md
%{_includedir}/websocketpp
%{_datadir}/cmake/websocketpp
%{_npkgconfigdir}/websocketpp.pc
