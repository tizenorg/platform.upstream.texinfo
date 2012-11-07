Name:           texinfo
Version:        4.13a
Release:        0
License:        GPL-2.0+ ; GPL-3.0+
Summary:        Tools Needed to Create Documentation from Texinfo Sources
Url:            http://www.texinfo.org
Group:          Productivity/Publishing/Texinfo
Source:         ftp://ftp.gnu.org/pub/gnu/texinfo/texinfo-%{version}.tar.bz2
Source1:        http://download.savannah.nongnu.org/releases/texi2html/texi2html-%{version_t2h}.tar.bz2
# texinfo.org: the domain is expired.
# http://texinfo.org/texi2roff/texi2roff-%{version_t2r}.tar.bz2
Source2:        texi2roff-%{version_t2r}.tar.bz2
Source10:       info-dir
Patch0:         texinfo-4.12.dif
Patch1:         texi2html-1.78.dif
Patch2:         texi2roff-2.0.dif
Patch3:         texi2roff.patch.bz2
Patch4:         texinfo-4.12-zlib.patch
Patch5:         texinfo-4.8-echo.patch
Patch6:         texi2roff-2.0-gcc4.patch
Patch7:         texinfo-4.13a-bug640417.diff
Patch8:         texinfo-4.13a-bug713517.diff
Patch9:         automake-1.12.patch
BuildRequires:  automake
BuildRequires:  bzip2-devel
BuildRequires:  help2man
BuildRequires:  libzio-devel
BuildRequires:  ncurses-devel
BuildRequires:  perl-gettext
BuildRequires:  zlib-devel
Provides:       texi2html = %{version_t2h}
Provides:       texi2roff = %{version_t2r}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%global         version_t2h 1.82
%global         version_t2r 2.0

%description
Texinfo is a documentation system that uses a single source file to
produce both online information and printed output.  Using Texinfo, you
can create a printed document with the normal features of a book,
including chapters, sections, cross-references, and indices.  From the
same Texinfo source file, you can create a menu-driven, online info
file with nodes, menus, cross-references, and indices using the included
makeinfo tool.

Aggregated with texinfo in this package is texi2html and texi2roff.

%package -n info
License:        GPL-3.0+
Summary:        A Stand-Alone Terminal-Based Info Browser
Group:          Productivity/Publishing/Texinfo
Requires(pre):  bash
Requires(pre):  libzio
Requires(pre):  zlib

%description -n info
Info is a terminal-based program for reading documentation of computer
programs in the Info format. The GNU Project distributes most of its
on-line manuals in the Info format, so you need a program called "Info
reader" to read the manuals.

%package -n makeinfo
License:        GPL-3.0+
Summary:        Translate Texinfo documents to info format
Group:          Productivity/Publishing/Texinfo
Suggests:       texinfo
Provides:       texinfo:/usr/bin/makeinfo

%description -n makeinfo
Makeinfo translates  Texinfo source documentation to various other
formats, by default Info files suitable for reading online with Emacs
or standalone GNU Info.

%prep
rm -rf texi2html-%{version_t2h} texi2roff-%{version_t2r}
%setup -q -b 1 -b 2 -n texinfo-4.13
%patch4 -p0 -b .zlib
%patch5 -p0 -b .echo
%patch7 -p1 -b .size_t
%patch8 -p0 -b .egrep
%patch9 -p1
%patch0 -p0
pushd ../texi2html-%{version_t2h}
%patch1 -p0
popd
pushd ../texi2roff-%{version_t2r}
%patch3 -p0 -b .Bader
%patch2 -p0
%patch6 -p1
popd

%build
    HOST=%{_target_cpu}-tizen-linux
    CFLAGS="%{optflags} -pipe"
    LDFLAGS=""
    CC=gcc
    export CFLAGS LDFLAGS CC
    export LD_AS_NEEDED=0
    AUTOPOINT=true autoreconf -fi
    ./configure --build=$HOST		\
	--prefix=%{_prefix}		\
	--mandir=%{_mandir}		\
	--datadir=%{_datadir}		\
	--infodir=%{_infodir}		\
	--without-included-gettext	\
	--enable-nls
    PATH=${PWD}/makeinfo:${PWD}/util:$PATH
    export PATH
    make %{?_smp_mflags};
pushd ../texi2html-%{version_t2h}
    ./configure --build=$HOST		\
	--prefix=%{_prefix}		\
	--mandir=%{_mandir}		\
	--datadir=%{_datadir}		\
	--infodir=%{_infodir}		\
	--without-included-gettext	\
	--enable-nls
    make %{?_smp_mflags};
popd
pushd ../texi2roff-%{version_t2r}
    rm -f texi2roff
    make %{?_smp_mflags};
popd

%install
    export LD_AS_NEEDED=0
    make DESTDIR=%{buildroot} \
	infodir=%{_infodir}	   \
	htmldir=%{_defaultdocdir}/texi2html install
    mkdir -p %{buildroot}/sbin
    mv %{buildroot}%{_bindir}/install-info %{buildroot}/sbin/
    ln -sf ../../sbin/install-info %{buildroot}%{_bindir}/install-info
    mkdir -p %{buildroot}%{_infodir}
    install -m 644 %{SOURCE10}       %{buildroot}%{_infodir}/dir
pushd ../texi2html-%{version_t2h}
    make DESTDIR=%{buildroot} \
	infodir=%{_infodir}	   \
	texinfohtmldir=%{_defaultdocdir}/texi2html install
    install -m 644 README        %{buildroot}%{_defaultdocdir}/texi2html/
    install -m 644 NEWS          %{buildroot}%{_defaultdocdir}/texi2html/
    install -m 644 COPYING       %{buildroot}%{_defaultdocdir}/texi2html/
popd
pushd ../texi2roff-%{version_t2r}
    doc=%{_defaultdocdir}/texi2roff
    install -m 755 texi2roff     %{buildroot}%{_bindir}/
    install -m 755 texi2index    %{buildroot}%{_bindir}/
    install -m 644 texi2roff.1   %{buildroot}%{_mandir}/man1/
    mkdir -p                     %{buildroot}${doc}
    install -m 644 Readme        %{buildroot}${doc}
    install -m 644 copyright     %{buildroot}${doc}
popd
%find_lang %{name} %{name}.lang

%files
%defattr(-, root, root)
%dir %{_defaultdocdir}/texi2html
%dir %{_defaultdocdir}/texi2roff
%doc ABOUT-NLS AUTHORS COPYING INTRODUCTION NEWS README TODO
%doc doc/texinfo.tex doc/txi-*.tex
%doc %{_defaultdocdir}/texi2html/*
%doc %{_defaultdocdir}/texi2roff/*
%{_bindir}/pdftexi*
%{_bindir}/texi*
%{_infodir}/texinfo*.gz
%{_infodir}/texi2html*.gz
%{_mandir}/man1/pdftexi2dvi.1.gz
%{_mandir}/man1/texi*.1.gz
%{_mandir}/man5/texinfo.5.gz
%{_datadir}/texinfo
%{_datadir}/texi2html

%files -n makeinfo -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/makeinfo
%{_mandir}/man1/makeinfo.1.gz

%files -n info
%defattr(-,root,root)
%config(noreplace) %verify(not md5 size mtime) %{_infodir}/dir
/sbin/install-info
%{_bindir}/install-info
%{_bindir}/info
%{_bindir}/infokey
%{_infodir}/info.info*
%{_infodir}/info-stnd.info*
%{_mandir}/man1/info.1*
%{_mandir}/man1/infokey.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*

%changelog
