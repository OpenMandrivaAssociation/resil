%define oname ResIL
%define major 1
%define libIL %mklibname IL %{major}
%define libILU %mklibname ILU %{major}
%define libILUT %mklibname ILUT %{major}
%define devname %mklibname %{name} -d
%define olddevname %mklibname devil -d

Summary:	Open source image library
Name:		resil
Version:	1.8.2
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://resil.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/resil/%{version}/%{oname}-%{version}.zip
Patch0:		ResIL-1.8.2-fix-buildsystem.patch
Patch1:		ResIL-1.8.2-compile.patch
Patch2:		ResIL-1.8.2-avoid-bogus-allegro-headers.patch
Patch3:		ResIL-1.8.2-fix-EXR.patch
Patch4:		ResIL-1.8.2-lcms2-on-unix.patch
BuildRequires:	file
BuildRequires:	libtool
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libmng)
BuildRequires:	tiff-devel
BuildRequires:	giflib-devel
BuildRequires:	pkgconfig(allegro)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	texinfo

%description
ResIL (continuation of DevIL project) is an Open Source image library whose
distribution is done under the terms of the GNU LGPL license.
ResIL offers you a simple way to implement loading, manipulating, filtering,
converting, displaying, saving from/to several different image formats in your
own project.

%package 	utils
Summary:	Tools provided by %{oname}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
%rename		devil-utils

%description	utils
This package contains tools provided by %{oname}.

%package -n %{libIL}
Summary:	Libraries needed for programs using %{oname}
Group:		System/Libraries
Obsoletes:	%{_lib}devil1 < %{version}-%{release}

%description -n	%{libIL}
This package contains the shared library for %{oname}.

%package -n %{libILU}
Summary:	Libraries needed for programs using %{oname}
Group:		System/Libraries
Conflicts:	%{_lib}devil1 < %{version}-%{release}

%description -n	%{libILU}
This package contains the shared library for %{oname}.

%package -n %{libILUT}
Summary:	Libraries needed for programs using %{oname}
Group:		System/Libraries
Conflicts:	%{_lib}devil1 < %{version}-%{release}

%description -n	%{libILUT}
This package contains the shared library for %{oname}.

%package -n %{devname}
Summary:	Development headers and libraries for writing programs using %{oname}
Group:		Development/C
Requires:	%{libIL} = %{version}-%{release}
Requires:	%{libILU} = %{version}-%{release}
Requires:	%{libILUT} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
%define __noautoreq 'devel\\(liballeg.*'
Obsoletes:	%{_lib}devel-static-devel = %{version}-%{release}
%rename		%{olddevname}

%description -n	%{devname}
Development headers and libraries for writing programs using %{oname}.

%prep
%setup -qn %{oname}-%{version}
%apply_patches

# Funny 0000 permissions...
chmod -R 0777 Input\ Libs/zlib128-dll
# Remove useless bloat
rm -rf \
	Input\ Libs

chmod 644 AUTHORS CREDITS ChangeLog README.unix

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
chmod +x configure

aclocal -I m4
autoheader
automake -a
autoconf

%build
export CFLAGS="%{optflags} -O3 -funroll-loops -ffast-math -fomit-frame-pointer -fexpensive-optimizations"

%configure	\
	--disable-static \
	--enable-shared \
	--enable-ILU \
	--enable-ILUT \
%ifarch x86_64
	--enable-x86_64 \
	--enable-sse \
	--enable-sse2 \
	--disable-sse3 \
%else
%ifarch %ix86
	--enable-x86 \
	--disable-x86_64
	--disable-sse \
	--disable-sse2 \
	--disable-sse3 \
%endif
%endif
	--with-x \
	--with-zlib=yes \
	--enable-release

# Not ready for SMP make as of 1.8.2
make

%install
%makeinstall_std

%files utils
%{_bindir}/ilur

%files -n %{libIL}
%{_libdir}/libIL.so.%{major}*

%files -n %{libILU}
%{_libdir}/libILU.so.%{major}*

%files -n %{libILUT}
%{_libdir}/libILUT.so.%{major}*

%files -n %{devname}
%doc AUTHORS CREDITS ChangeLog README.unix
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/IL
%{_infodir}/*.info.*

