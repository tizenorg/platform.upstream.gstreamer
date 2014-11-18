%bcond_with introspection

Name:           gstreamer
Version:        1.4.1
Release:        0
%define gst_branch 1.0
Summary:        Streaming-Media Framework Runtime
License:        LGPL-2.1+
Group:          Multimedia/Framework
Url:            http://gstreamer.freedesktop.org/
Source0:        http://download.gnome.org/sources/gstreamer/1.0/%{name}-%{version}.tar.xz
Source1:        gstreamer.macros
Source2:        gstreamer.prov
Source99:       baselibs.conf
Source100:      common.tar.bz2
Source1001: 	gstreamer.manifest
BuildRequires:  bison
BuildRequires:	gettext-tools
BuildRequires:  check-devel
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  glib2-devel >= 2.32.0
BuildRequires:  libtool
BuildRequires:  gst-common
BuildRequires:  libxml2-devel
%if %{with introspection}
BuildRequires:  gobject-introspection-devel >= 1.31.1
%endif
Requires:       libgstreamer >= %{version}

%description
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related.  Its plug-in-based architecture
means that new data types or processing capabilities can be added by
installing new plug-ins.

%package -n libgstreamer
Summary:        Streaming-Media Framework Runtime
Group:          Multimedia/Framework
# We want to have core modules installed:
Requires:       %{name}

%description -n libgstreamer
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related.  Its plug-in-based architecture
means that new data types or processing capabilities can be added by
installing new plug-ins.

%package -n typelib-Gst
Summary:        Streaming-Media Framework Runtime -- Introspection bindings
Group:          Multimedia/Framework

%description -n typelib-Gst
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related.  Its plug-in-based architecture
means that new data types or processing capabilities can be added by
installing new plug-ins.

This package provides the GObject Introspection bindings for GStreamer.

%package utils
Summary:        Streaming-Media Framework Runtime
Group:          Multimedia/Framework
Provides:       gstreamer:%{_bindir}/gst-launch-%{gst_branch} = %{version}
# Symbol for unversioned wrappers:
Provides:       gstreamer-utils_versioned = %{version}

%description utils
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related.  Its plug-in-based architecture
means that new data types or processing capabilities can be added by
installing new plug-ins.

%package devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
Requires:       %{name} = %{version}
# gstreamer-utils is required for the gstreamer-provides rpm magic.
Requires:       gstreamer-utils = %{version}
Requires:       libgstreamer = %{version}
%if %{with introspection}
Requires:       typelib-Gst = %{version}
%endif

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%lang_package

%prep
%setup -q -n gstreamer-%{version}
%setup -q -T -D -a 100
cp %{SOURCE1001} .

%build
# FIXME: GTKDOC_CFLAGS, GST_OBJ_CFLAGS:
# Silently ignored compilation of uninstalled gtk-doc scanners without RPM_OPT_FLAGS.
export V=1
NOCONFIGURE=1 ./autogen.sh
export CFLAGS="%{optflags} -fno-strict-aliasing"
%configure\
%if %{with introspection}
        --enable-introspection\
%endif
	--disable-static
make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}%{_datadir}/gstreamer-%{gst_branch}/presets
mkdir -p %{buildroot}%{_docdir}/%{name}
%find_lang %{name}-%{gst_branch}
mv %{name}-%{gst_branch}.lang %{name}.lang
rm -rf %{buildroot}%{_datadir}/gtk-doc
rm -rf %{buildroot}%{_docdir}/%{name}/manual
rm -rf %{buildroot}%{_docdir}/%{name}/pwg
mkdir -p %{buildroot}%{_datadir}/gstreamer-%{gst_branch}/presets
%__install -m644 -D %{S:1} %{buildroot}%{_libexecdir}/rpm/fileattrs/gstreamer.attr
%__install -m755 -D %{S:2} %{buildroot}%{_libexecdir}/rpm/gstreamer-provides
%fdupes %{buildroot}


%post -n libgstreamer -p /sbin/ldconfig

%postun -n libgstreamer -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%dir %{_datadir}/gstreamer-%{gst_branch}
%dir %{_datadir}/gstreamer-%{gst_branch}/presets
%dir %{_libdir}/gstreamer-%{gst_branch}
%{_libdir}/gstreamer-%{gst_branch}/*.so
%dir %{_libexecdir}/gstreamer-%{gst_branch}
%{_libexecdir}/gstreamer-%{gst_branch}/gst-plugin-scanner

%files -n libgstreamer
%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/*.so.*


%if %{with introspection}
%files -n typelib-Gst
%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/girepository-1.0/Gst-1.0.typelib
%{_libdir}/girepository-1.0/GstBase-1.0.typelib
%{_libdir}/girepository-1.0/GstCheck-1.0.typelib
%{_libdir}/girepository-1.0/GstController-1.0.typelib
%{_libdir}/girepository-1.0/GstNet-1.0.typelib
%endif

%files utils
%manifest %{name}.manifest
%defattr(-, root, root)
%{_bindir}/*-%{gst_branch}
%doc %{_mandir}/man?/*-%{gst_branch}.*

%files devel
%manifest %{name}.manifest
%defattr(-, root, root)
%{_datadir}/aclocal/*.m4
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libexecdir}/rpm/gstreamer-provides
%{_libexecdir}/rpm/fileattrs/gstreamer.attr
%if %{with introspection}
%{_datadir}/gir-1.0/*.gir
%endif

%changelog
