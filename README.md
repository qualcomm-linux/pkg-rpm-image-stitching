<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# pkg-rpm-image-stitching

RPM packaging for the Qualcomm® Linux dynamic image-stitching library and
development files.

This repository contains RPM packaging rules for the
`qcom-image-stitching` prebuilt release. The package provides the
`libimage_stitching.so` runtime library, the public `image_stitching.h` and
`mesh_fusion.h` headers, and the `nv12_blend.cl` OpenCL kernel.

The prebuilt archive is fetched during the RPM build from Qualcomm Software
Center. This repository contains no compiled libraries, binaries, or source
archives.

The `main` branch contains repository documentation and workflow support files.

## License

This project is licensed under the BSD 3-Clause License. See
[LICENSE.txt](LICENSE.txt) for the complete license text.
