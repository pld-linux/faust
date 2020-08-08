#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests
#
Summary:	Faust - Programming Language for Audio Applications and Plugins
Name:		faust
Version:	2.20.2
%define		libsrev	127e5bf
Release:	1
License:	GPL v2 and BSD
Group:		Applications/Multimedia
# SF URL: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source0:	https://github.com/grame-cncm/faust/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2e4f2db77a1229edf7eb18f14ddd6617
Source1:	https://github.com/grame-cncm/faustlibraries/archive/%{libsrev}/%{name}libraries-%{version}-%{libsrev}.tar.gz
# Source1-md5:	a0402ea3d24a3fcfb2b8e2e5f251e329
Patch0:		libmicrohttpd.patch
Patch1:		libdir.patch
URL:		https://faust.grame.fr/
BuildRequires:	cmake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_noautostrip	.*/.*libsndfile\..*

%description
Faust (Functional Audio Stream) is a functional programming language
for sound synthesis and audio processing with a strong focus on
the design of synthesizers, musical instruments, audio effects, etc.
Faust targets high-performance signal processing applications and
audio plug-ins for a variety of platforms and standards.

%package android
Summary:	Faust API support for android
Group:		Applications/Multimedia

%description android
Faust API support for android.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1

%{__mv} faustlibraries-%{libsrev}*/* libraries/
%{__rm} -r faustlibraries-%{libsrev}*

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
      tools/faust2appls/faust2atomsnippets \
      tools/faust2appls/faust2md

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+ruby(\s|$),#!%{__ruby}\1,' \
      tools/faust2sc-1.0.0/faust2sc

%build
CMAKEOPT="\
	-DCMAKE_VERBOSE_MAKEFILE=ON \
	-DCMAKE_BUILD_TYPE=%{!?debug:PLD}%{?debug:Debug} \
	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
	-DCMAKE_CXX_FLAGS_PLD='%{rpmcxxflags}' \
	-DCMAKE_C_FLAGS_PLD='%{rpmcflags}' \
	-DCMAKE_Fortran_FLAGS_PLD='%{rpmcflags}' \
	-DCMAKE_EXE_LINKER_FLAGS_PLD='%{rpmldflags}' \
	-DCMAKE_SHARED_LINKER_FLAGS_PLD='%{rpmldflags}' \
	-DCMAKE_MODULE_LINKER_FLAGS_PLD='%{rpmldflags}'"

%{__make} \
	JOBS=%{?_smp_mflags} \
	PREFIX=%{_prefix} \
	LIBSDIR=%{_lib} \
	CMAKEOPT="$CMAKEOPT"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PREFIX=%{_prefix} \
	LIBSDIR=%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md WHATSNEW.md
%attr(755,root,root) %{_bindir}/%{name}*
%attr(755,root,root) %{_bindir}/encoderunitypackage
%attr(755,root,root) %{_bindir}/filename2ident
%attr(755,root,root) %{_bindir}/sound2reader
%{_datadir}/faust
%{_mandir}/man1/faust.1*

%exclude %{_datadir}/faust/android
%exclude %{_datadir}/faust/api/android
%exclude %{_datadir}/faust/smartKeyboard/android

%files android
%defattr(644,root,root,755)
%{_datadir}/faust/android
%{_datadir}/faust/api/android
%{_datadir}/faust/smartKeyboard/android

%files devel
%defattr(644,root,root,755)
%{_includedir}/faust
%{_libdir}/*.a
