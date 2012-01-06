
Name:       gstreamer
Summary:    GStreamer streaming media framework runtime
Version:    0.10.34
Release:    1
Group:      Applications/Multimedia
License:    LGPLv2+
URL:        http://gstreamer.freedesktop.org/
Source0:    http://gstreamer.freedesktop.org/src/gstreamer/%{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(mm-ta)
BuildRequires:  bison
BuildRequires:  flex


%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.



%package devel
Summary:    Development tools for GStreamer
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains the libraries and includes files necessary to develop
applications and plugins for GStreamer. If you plan to develop applications
with GStreamer, consider installing the gstreamer-devel-docs package and the
documentation packages for any plugins you intend to use.


%package tools
Summary:    Common tools and files for GStreamer streaming media framework
Group:      Applications/Multimedia
Requires:   %{name} = %{version}-%{release}

%description tools
This package contains wrapper scripts for the command-line tools that work
with different major/minor versions of GStreamer.



%prep
%setup -q -n %{name}-%{version}


%build


export CFLAGS+=" -Wall -g -fPIC				
		-DGST_EXT_COMPANSATE_EOS_HANDLING	\
		-DGST_EXT_USE_TINY_REGISTRY		\
		-DGST_EXT_TIME_ANALYSIS 		\
		-DGST_EXT_TA_UNIT_MEXT 			\
		-DGST_EXT_PAD_LINK_UNCHECKED		\
		-DGST_EXT_REDUCE_PLUGIN_NUM 		\
		-DGST_EXT_USE_PDP_NETWORK		\
		-DGST_EXT_VOLUME_WITHOUT_LIBOIL 	\
		-DGST_EXT_AUDIOSINK_MUTE 		\
		-DEXT_AUDIO_FILTER_EFFECT 		\
		-DGST_EXT_NONBLOCKDQUE			\
		-DGST_EXT_RENEGOTIATION			\
		-DGST_EXT_MOBILECAMERA 			\
		-DGST_EXT_ASYNC_DEV			\
		-DGST_EXT_AV_RECORDING 			\
		-DGST_EXT_SWITCH_CAMERA 		\
		-DGST_EXT_OVERLAYSINK_SQVGA 		\
		-DGST_EXT_FFMUX_ADD_PROPERTY 		\
		-DGST_EXT_FFMUX_ENHANCEMENT 		\
		-DGST_EXT_I_LIKE_DSP			\
		-DGST_EXT_CAMCORDER_IPP			\
		-DGST_EXT_QUEUE_ENHANCEMENT"

%configure --prefix=/usr		\
		--disable-valgrind			\
		--without-check 			\
		--disable-static 			\
		--disable-rpath 			\
		--disable-libtool-lock 		\
		--disable-alloc-trace 		\
		--disable-gcov 			\
		--disable-nls 			\
		--disable-examples 		\
		--disable-tests 			\
		--disable-failing-tests 		\
		--disable-docbook 		\
		--disable-gtk-doc 		\
		--disable-registry-update 	\
		--disable-loadsave 		\
		--with-html-dir=/tmp/dump 	\
		CFLAGS="$(CFLAGS)" 	\
		LDFLAGS="$(LDFLAGS)"

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

rm -rf %{buildroot}/tmp/dump


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig











%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README RELEASE TODO
%{_libdir}/libgstreamer-0.10.so.*
%{_libdir}/libgstbase-0.10.so.*
%{_libdir}/libgstcontroller-0.10.so.*
%{_libdir}/libgstdataprotocol-0.10.so.*
%{_libdir}/libgstnet-0.10.so.*
%{_libdir}/libgstcheck-0.10.so.*
%dir %{_libdir}/gstreamer-0.10
%{_libdir}/gstreamer-0.10/libgstcoreelements.so
%{_libdir}/gstreamer-0.10/libgstcoreindexers.so
%dir %{_libexecdir}/gstreamer-0.10
%{_libexecdir}/gstreamer-0.10/gst-plugin-scanner
%{_bindir}/gst-feedback-0.10
%{_bindir}/gst-inspect-0.10
%{_bindir}/gst-launch-0.10
%{_bindir}/gst-typefind-0.10
%{_bindir}/gst-xmlinspect-0.10
%doc %{_mandir}/man1/gst-feedback-0.10.*
%doc %{_mandir}/man1/gst-inspect-0.10.*
%doc %{_mandir}/man1/gst-launch-0.10.*
%doc %{_mandir}/man1/gst-typefind-0.10.*
%doc %{_mandir}/man1/gst-xmlinspect-0.10.*


%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/gstreamer-0.10
%dir %{_includedir}/gstreamer-0.10/gst
%{_includedir}/gstreamer-0.10/gst/*.h
%{_includedir}/gstreamer-0.10/gst/base
%{_includedir}/gstreamer-0.10/gst/check
%{_includedir}/gstreamer-0.10/gst/controller
%{_includedir}/gstreamer-0.10/gst/dataprotocol
%{_includedir}/gstreamer-0.10/gst/net
%{_datadir}/aclocal/gst-element-check-0.10.m4
%{_libdir}/libgstreamer-0.10.so
%{_libdir}/libgstbase-0.10.so
%{_libdir}/libgstcontroller-0.10.so
%{_libdir}/libgstdataprotocol-0.10.so
%{_libdir}/libgstnet-0.10.so
%{_libdir}/libgstcheck-0.10.so
%{_libdir}/pkgconfig/gstreamer-0.10.pc
%{_libdir}/pkgconfig/gstreamer-base-0.10.pc
%{_libdir}/pkgconfig/gstreamer-controller-0.10.pc
%{_libdir}/pkgconfig/gstreamer-check-0.10.pc
%{_libdir}/pkgconfig/gstreamer-dataprotocol-0.10.pc
%{_libdir}/pkgconfig/gstreamer-net-0.10.pc

%files tools
%defattr(-,root,root,-)
%{_bindir}/gst-feedback
%{_bindir}/gst-inspect
%{_bindir}/gst-launch
%{_bindir}/gst-typefind
%{_bindir}/gst-xmlinspect
#%{_bindir}/gst-xmllaunch

