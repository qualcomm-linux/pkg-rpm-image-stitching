# RPM packaging for the image-stitching prebuilt binary drop.

%global vendor_arch             aarch64
%global vendor_dist             el10
%global vendor_build_date       261110

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

Source0:        https://softwarecenter.qualcomm.com/nexus/generic/software/chip/component/iot-core-algs.lnx.0.0/%{vendor_build_date}/prebuilt_rpm/qcom-image-stitching-%{version}.%{vendor_dist}.%{vendor_arch}.tar.gz

ExclusiveArch:  aarch64

%description
QCOM library for dynamic image stitching with OpenCV and OpenCL support.

The package contains the prebuilt image-stitching shared library for
Qualcomm platforms.

%package devel
Summary:        QCOM Dynamic Image Stitching Library - Development files
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       qcom-image-stitching-dev = %{version}-%{release}

%description devel
Development headers and the unversioned linker symlink for the QCOM dynamic
image-stitching library.

%prep
%autosetup -c -n %{name}-%{version} -p1

for f in usr/LICENSE.qcom-2 \
         usr/NOTICE \
         usr/VERSION \
         usr/include/image_stitching.h \
         usr/include/mesh_fusion.h \
         usr/lib/libimage_stitching.so.1.0; do
    if [ ! -e "$f" ]; then
        echo "ERROR: expected '$f' in %{SOURCE0}" >&2
        echo "ERROR: the vendor tarball layout changed; update this spec." >&2
        exit 1
    fi
done

vendor_version="$(tr -d '[:space:]' < usr/VERSION)"
if [ "$vendor_version" != "%{version}" ]; then
    echo "ERROR: vendor VERSION '$vendor_version' does not match spec Version '%{version}'" >&2
    exit 1
fi

# Stage the vendor license and notice files at the top level for %%license and %%doc.
cp -p usr/LICENSE.qcom-2 usr/NOTICE .

%build

%install
install -d -m 0755 %{buildroot}%{_libdir}
install -d -m 0755 %{buildroot}%{_includedir}

install -p -m 0755 usr/lib/libimage_stitching.so.1.0 \
    %{buildroot}%{_libdir}/libimage_stitching.so.1.0
ln -s libimage_stitching.so.1.0 %{buildroot}%{_libdir}/libimage_stitching.so.1
ln -s libimage_stitching.so.1 %{buildroot}%{_libdir}/libimage_stitching.so
install -p -m 0644 usr/include/image_stitching.h usr/include/mesh_fusion.h \
    %{buildroot}%{_includedir}/

%check
:

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE.qcom-2
%doc NOTICE
%{_libdir}/libimage_stitching.so.1
%{_libdir}/libimage_stitching.so.1.0

%files devel
%{_libdir}/libimage_stitching.so
%{_includedir}/image_stitching.h
%{_includedir}/mesh_fusion.h

%changelog
* Fri Oct 09 2026 Qualcomm Linux Packaging <linux@qti.qualcomm.com> - 1.0.0-1
- Initial RPM packaging
- Package the qcom-image-stitching-1.0.0.el10.aarch64 prebuilt binary drop
- Split the public image-stitching headers into qcom-image-stitching-devel
