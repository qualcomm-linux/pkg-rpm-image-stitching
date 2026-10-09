<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# pkg-rpm-qcom-image-stitching

RPM packaging for the Qualcomm dynamic image-stitching library and its public
development headers.

This repository packages the `qcom-image-stitching` RPM from the
`image-stitching` prebuilt binary release. The
runtime package contains `libimage_stitching.so` and the `nv12_blend.cl`
OpenCL kernel. The `qcom-image-stitching-devel` package contains the public
`image_stitching.h` and `mesh_fusion.h` headers.

The prebuilt archive is fetched during the RPM build from Qualcomm Software
Center. This repository contains no compiled libraries, binaries, or source
archives. The `meta-aimm-fwks.lnx.0.0` component release dated `261006` is
referenced by `Source0` in the spec, and the checksum in `sources` is verified
before the RPM is built.

## Repository Layout

| File | Purpose |
|---|---|
| `qcom-image-stitching.spec` | Builds the runtime and development RPM packages. |
| `sources` | SHA-512 checksum for the prebuilt image-stitching archive. |
| `.github/workflows/build-on-pr.yml` | Builds the RPM packages for pull requests. |
| `.github/workflows/pkg-release.yml` | Builds and publishes release RPMs. |
| `README.md` | Package and repository documentation. |
| `LICENSE.txt` | License for the RPM packaging repository. |

## Packages

### `qcom-image-stitching`

Runtime package containing the prebuilt image-stitching shared library and its
OpenCL kernel under `/usr/lib64/image_stitching`. The shared library uses
OpenCV and OpenCL runtime libraries supplied by the target Qualcomm Linux
image; its ELF dependencies are recorded automatically by RPM.

### `qcom-image-stitching-devel`

Development package providing the public headers under
`/usr/include/image_stitching`.

The packages are built for `aarch64`; the vendor archive is not compiled or
stripped during the RPM build.

## Installation

Install the runtime and development packages from the configured CentOS Stream
10 repository:

```bash
sudo dnf install -y qcom-image-stitching qcom-image-stitching-devel
```

## Updating the Package Version

1. Update `Version:` and `vendor_build_date` in `qcom-image-stitching.spec`, and
   update `Source0` if the Qualcomm Software Center artifact location changes.
   The archive filename must remain
   `image-stitching_<version>_armv8a.tar.gz`.
2. Confirm that the staged archive still contains the files validated by the
   `%prep` checks in the spec.
3. Regenerate the source checksum:

   ```bash
   sha512sum --tag image-stitching_<version>_armv8a.tar.gz > sources
   ```

4. Commit the spec and `sources`, then open a pull request against `c10s`.
5. After the pull request is merged, run `pkg-release.yml` to publish the
   RPMs.

## License

This packaging repository is licensed under the BSD 3-Clause License. See
`LICENSE.txt` for the complete license text.

The vendor binary payload is distributed under Qualcomm's binary license. The
`LICENSE.qcom-2` file from the vendor archive is included in the runtime RPM.
