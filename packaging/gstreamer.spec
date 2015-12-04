%define gst_branch 1.0

Name:           gstreamer
Version:        1.6.1
Release:        3
Summary:        Streaming-Media Framework Runtime
License:        LGPL-2.1+
Group:          Multimedia/Framework
Url:            http://gstreamer.freedesktop.org/
Source0:        http://gstreamer.freedesktop.org/src/gstreamer/gstreamer-%{version}.tar.xz
Source100:      common.tar.gz
BuildRequires:  bison
BuildRequires:  gettext-tools
BuildRequires:  check-devel
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  glib2-devel >= 2.32
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  gobject-introspection-devel >= 1.31.1
BuildRequires:  pkgconfig(dlog)
BuildRequires:  gcc-c++
BuildRequires:  orc >= 0.4.16
BuildRequires:  python

%description
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related.  Its plug-in-based architecture
means that new data types or processing capabilities can be added by
installing new plug-ins.

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
# gstreamer-utils is required for the gstreamer-provides rpm magic.
Requires:       gstreamer-utils = %{version}
Requires:       %{name} = %{version}

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%lang_package

%prep
%setup -q -n gstreamer-%{version}
%setup -q -T -D -a 100

%build
# FIXME: GTKDOC_CFLAGS, GST_OBJ_CFLAGS:
# Silently ignored compilation of uninstalled gtk-doc scanners without RPM_OPT_FLAGS.
export V=1
NOCONFIGURE=1 ./autogen.sh
export CFLAGS="%{optflags} \
	-DGST_QUEUE2_MODIFICATION\
	-DGST_EXT_CURRENT_BYTES\
	-DGST_TIZEN_MODIFICATION\
	-fno-strict-aliasing"

%configure\
        --enable-introspection\
        --disable-static\
        --enable-dlog\
        --disable-examples
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
%fdupes %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING

%dir %{_datadir}/gstreamer-%{gst_branch}
%dir %{_datadir}/gstreamer-%{gst_branch}/presets
%dir %{_libdir}/gstreamer-%{gst_branch}
%dir %{_libexecdir}/gstreamer-%{gst_branch}

%define so_version so.0.601.0
%define so_version_debug %{so_version}.debug
%define _lib_gstreamer_dir %{_libdir}/gstreamer-%{gst_branch}

%{_lib_gstreamer_dir}/libgstcoreelements.so

%{_libdir}/libgstbase-%{gst_branch}.so
%{_libdir}/libgstcheck-%{gst_branch}.so
%{_libdir}/libgstcontroller-%{gst_branch}.so
%{_libdir}/libgstnet-%{gst_branch}.so
%{_libdir}/libgstreamer-%{gst_branch}.so

%{_libdir}/libgstbase-%{gst_branch}.so.0
%{_libdir}/libgstcheck-%{gst_branch}.so.0
%{_libdir}/libgstcontroller-%{gst_branch}.so.0
%{_libdir}/libgstnet-%{gst_branch}.so.0
%{_libdir}/libgstreamer-%{gst_branch}.so.0

%{_libdir}/libgstbase-%{gst_branch}.%{so_version}
%{_libdir}/libgstcheck-%{gst_branch}.%{so_version}
%{_libdir}/libgstcontroller-%{gst_branch}.%{so_version}
%{_libdir}/libgstnet-%{gst_branch}.%{so_version}
%{_libdir}/libgstreamer-%{gst_branch}.%{so_version}

%{_libdir}/girepository-1.0/Gst-%{gst_branch}.typelib
%{_libdir}/girepository-1.0/GstBase-%{gst_branch}.typelib
%{_libdir}/girepository-1.0/GstCheck-%{gst_branch}.typelib
%{_libdir}/girepository-1.0/GstController-%{gst_branch}.typelib
%{_libdir}/girepository-1.0/GstNet-%{gst_branch}.typelib

%{_lib_gstreamer_dir}/include/gst/gstconfig.h
%{_libexecdir}/gstreamer-%{gst_branch}/gst-plugin-scanner
%{_libexecdir}/gstreamer-%{gst_branch}/gst-ptp-helper

%files utils
%manifest %{name}.manifest
%{_bindir}/gst-inspect-%{gst_branch}
%{_bindir}/gst-launch-%{gst_branch}
%{_bindir}/gst-typefind-%{gst_branch}

%doc %{_mandir}/man?/*-%{gst_branch}.*

%define _gstinclude_dir %{_includedir}/gstreamer-%{gst_branch}/gst

%files devel
%manifest %{name}.manifest

%{_libdir}/libgstbase-%{gst_branch}.so
%{_libdir}/libgstcheck-%{gst_branch}.so
%{_libdir}/libgstcontroller-%{gst_branch}.so
%{_libdir}/libgstnet-%{gst_branch}.so
%{_libdir}/libgstreamer-%{gst_branch}.so

%{_libdir}/pkgconfig/gstreamer-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-base-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-check-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-controller-%{gst_branch}.pc
%{_libdir}/pkgconfig/gstreamer-net-%{gst_branch}.pc

%{_datadir}/aclocal/gst-element-check-1.0.m4

%define gir_dir gir-%{gst_branch}

%{_datadir}/%{gir_dir}/Gst-%{gst_branch}.gir
%{_datadir}/%{gir_dir}/GstBase-%{gst_branch}.gir
%{_datadir}/%{gir_dir}/GstCheck-%{gst_branch}.gir
%{_datadir}/%{gir_dir}/GstController-%{gst_branch}.gir
%{_datadir}/%{gir_dir}/GstNet-%{gst_branch}.gir

%{_gstinclude_dir}/base/base.h
%{_gstinclude_dir}/base/gstadapter.h
%{_gstinclude_dir}/base/gstbaseparse.h
%{_gstinclude_dir}/base/gstbasesink.h
%{_gstinclude_dir}/base/gstbasesrc.h
%{_gstinclude_dir}/base/gstbasetransform.h
%{_gstinclude_dir}/base/gstbitreader.h
%{_gstinclude_dir}/base/gstbytereader.h
%{_gstinclude_dir}/base/gstbytewriter.h
%{_gstinclude_dir}/base/gstcollectpads.h
%{_gstinclude_dir}/base/gstdataqueue.h
%{_gstinclude_dir}/base/gstflowcombiner.h
%{_gstinclude_dir}/base/gstpushsrc.h
%{_gstinclude_dir}/base/gstqueuearray.h
%{_gstinclude_dir}/base/gsttypefindhelper.h
%{_gstinclude_dir}/check/check.h
%{_gstinclude_dir}/check/gstbufferstraw.h
%{_gstinclude_dir}/check/gstcheck.h
%{_gstinclude_dir}/check/gstconsistencychecker.h
%{_gstinclude_dir}/check/gstharness.h
%{_gstinclude_dir}/check/gsttestclock.h
%{_gstinclude_dir}/check/internal-check.h
%{_gstinclude_dir}/controller/controller.h
%{_gstinclude_dir}/controller/gstargbcontrolbinding.h
%{_gstinclude_dir}/controller/gstdirectcontrolbinding.h
%{_gstinclude_dir}/controller/gstinterpolationcontrolsource.h
%{_gstinclude_dir}/controller/gstlfocontrolsource.h
%{_gstinclude_dir}/controller/gsttimedvaluecontrolsource.h
%{_gstinclude_dir}/controller/gsttriggercontrolsource.h
%{_gstinclude_dir}/glib-compat.h
%{_gstinclude_dir}/gst.h
%{_gstinclude_dir}/gstallocator.h
%{_gstinclude_dir}/gstatomicqueue.h
%{_gstinclude_dir}/gstbin.h
%{_gstinclude_dir}/gstbuffer.h
%{_gstinclude_dir}/gstbufferlist.h
%{_gstinclude_dir}/gstbufferpool.h
%{_gstinclude_dir}/gstbus.h
%{_gstinclude_dir}/gstcaps.h
%{_gstinclude_dir}/gstcapsfeatures.h
%{_gstinclude_dir}/gstchildproxy.h
%{_gstinclude_dir}/gstclock.h
%{_gstinclude_dir}/gstcompat.h
%{_gstinclude_dir}/gstcontext.h
%{_gstinclude_dir}/gstcontrolbinding.h
%{_gstinclude_dir}/gstcontrolsource.h
%{_gstinclude_dir}/gstdatetime.h
%{_gstinclude_dir}/gstdebugutils.h
%{_gstinclude_dir}/gstdevice.h
%{_gstinclude_dir}/gstdevicemonitor.h
%{_gstinclude_dir}/gstdeviceprovider.h
%{_gstinclude_dir}/gstdeviceproviderfactory.h
%{_gstinclude_dir}/gstelement.h
%{_gstinclude_dir}/gstelementfactory.h
%{_gstinclude_dir}/gstelementmetadata.h
%{_gstinclude_dir}/gstenumtypes.h
%{_gstinclude_dir}/gsterror.h
%{_gstinclude_dir}/gstevent.h
%{_gstinclude_dir}/gstformat.h
%{_gstinclude_dir}/gstghostpad.h
%{_gstinclude_dir}/gstinfo.h
%{_gstinclude_dir}/gstiterator.h
%{_gstinclude_dir}/gstmacros.h
%{_gstinclude_dir}/gstmemory.h
%{_gstinclude_dir}/gstmessage.h
%{_gstinclude_dir}/gstmeta.h
%{_gstinclude_dir}/gstminiobject.h
%{_gstinclude_dir}/gstobject.h
%{_gstinclude_dir}/gstpad.h
%{_gstinclude_dir}/gstpadtemplate.h
%{_gstinclude_dir}/gstparamspecs.h
%{_gstinclude_dir}/gstparse.h
%{_gstinclude_dir}/gstpipeline.h
%{_gstinclude_dir}/gstplugin.h
%{_gstinclude_dir}/gstpluginfeature.h
%{_gstinclude_dir}/gstpoll.h
%{_gstinclude_dir}/gstpreset.h
%{_gstinclude_dir}/gstprotection.h
%{_gstinclude_dir}/gstquery.h
%{_gstinclude_dir}/gstregistry.h
%{_gstinclude_dir}/gstsample.h
%{_gstinclude_dir}/gstsegment.h
%{_gstinclude_dir}/gststructure.h
%{_gstinclude_dir}/gstsystemclock.h
%{_gstinclude_dir}/gsttaglist.h
%{_gstinclude_dir}/gsttagsetter.h
%{_gstinclude_dir}/gsttask.h
%{_gstinclude_dir}/gsttaskpool.h
%{_gstinclude_dir}/gsttoc.h
%{_gstinclude_dir}/gsttocsetter.h
%{_gstinclude_dir}/gsttypefind.h
%{_gstinclude_dir}/gsttypefindfactory.h
%{_gstinclude_dir}/gsturi.h
%{_gstinclude_dir}/gstutils.h
%{_gstinclude_dir}/gstvalue.h
%{_gstinclude_dir}/gstversion.h
%{_gstinclude_dir}/math-compat.h
%{_gstinclude_dir}/net/gstnet.h
%{_gstinclude_dir}/net/gstnetaddressmeta.h
%{_gstinclude_dir}/net/gstnetclientclock.h
%{_gstinclude_dir}/net/gstnetcontrolmessagemeta.h
%{_gstinclude_dir}/net/gstnettimepacket.h
%{_gstinclude_dir}/net/gstnettimeprovider.h
%{_gstinclude_dir}/net/gstptpclock.h
%{_gstinclude_dir}/net/net.h

%changelog
