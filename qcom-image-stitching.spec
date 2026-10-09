# RPM packaging for the image-stitching prebuilt binary drop.

%global vendor_arch             armv8a
%global vendor_build_date       261006
%global image_stitching_libdir %{_libdir}/image_stitching
%global image_stitching_incdir %{_includedir}/image_stitching

# Keep the vendor aarch64 payload unchanged; the archive is not rebuilt here.
%global debug_package                   %{nil}
%global __strip                         /bin/true
%global __brp_strip                     %{nil}
%global __brp_strip_static_archive      %{nil}
%global __brp_strip_comment_note        %{nil}
%global _build_id_links                 none

Name:           qcom-image-stitching
Version:        1.0.0
Release:        1%{?dist}
Summary:        QCOM Dynamic Image Stitching Library

License:         BSD-3-Clause-Clear

Source0:        https://softwarecenter.qualcomm.com/nexus/generic/software/chip/component/meta-aimm-fwks.lnx.0.0/%{vendor_build_date}/prebuilt_yocto/image-stitching_%{version}_%{vendor_arch}.tar.gz

ExclusiveArch:  aarch64

%description
QCOM library for dynamic image stitching with OpenCV and OpenCL support.

The package contains the prebuilt image-stitching shared library and its
runtime OpenCL kernel for Qualcomm platforms.

%package devel
Summary:        QCOM Dynamic Image Stitching Library - Development files
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       qcom-image-stitching-dev = %{version}-%{release}

%description devel
Development headers for the QCOM dynamic image-stitching library.

%prep
%autosetup -c -n %{name}-%{version} -p1

for f in LICENSE.qcom-2 \
         usr/include/image_stitching/image_stitching.h \
         usr/include/image_stitching/mesh_fusion.h \
         usr/lib/image_stitching/libimage_stitching.so \
         usr/lib/image_stitching/nv12_blend.cl; do
    if [ ! -e "$f" ]; then
        echo "ERROR: expected '$f' in %{name}_%{version}_%{vendor_arch}.tar.gz" >&2
        echo "ERROR: the vendor tarball layout changed; update this spec." >&2
        exit 1
    fi
done

%build

%install
install -d -m 0755 %{buildroot}%{image_stitching_libdir}
install -d -m 0755 %{buildroot}%{image_stitching_incdir}

install -p -m 0755 usr/lib/image_stitching/libimage_stitching.so \
    %{buildroot}%{image_stitching_libdir}/libimage_stitching.so
install -p -m 0644 usr/lib/image_stitching/nv12_blend.cl \
    %{buildroot}%{image_stitching_libdir}/nv12_blend.cl
install -p -m 0644 usr/include/image_stitching/*.h \
    %{buildroot}%{image_stitching_incdir}/

%check
:

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE.qcom-2
%dir %{image_stitching_libdir}
%{image_stitching_libdir}/libimage_stitching.so
%{image_stitching_libdir}/nv12_blend.cl

%files devel
%dir %{image_stitching_incdir}
%{image_stitching_incdir}/image_stitching.h
%{image_stitching_incdir}/mesh_fusion.h

%changelog
* Fri Oct 09 2026 Qualcomm Linux Packaging <linux@qti.qualcomm.com> - 1.0.0-1
- Initial RPM packaging
- Package the image-stitching_1.0.0_armv8a prebuilt binary drop
- Split the public image-stitching headers into qcom-image-stitching-devel
