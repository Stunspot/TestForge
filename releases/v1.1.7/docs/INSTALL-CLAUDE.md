# Install TestForge in Claude

## Prerequisites

Python 3.10+ is recommended for the portable verifier but is not required by the skills at runtime. Without Python, follow the checksum and reduced-assurance path in the [quick start](QUICK-START.md).

- A Claude environment that exposes a supported custom-Skills upload or import control.
- Permission to add a Skill to that environment.
- The untouched ZIP for the handle you intend to use.

## Available archives

- [software-verification ZIP](../claude/software-verification-v1.1.7.zip)
- [verification-reviewer ZIP](../claude/verification-reviewer-v1.1.7.zip)

## Procedure

1. From the extracted release root, run `python tools/verify_release.py .` and require `"ok": true`.
2. Choose the ZIP whose filename matches the required handle. Do not unpack, recompress, or merge the ZIP.
3. In Claude's supported Skills manager or import control, upload that ZIP unchanged.
4. Confirm Claude reports the Skill as imported, then start a fresh chat.
5. Use the family starter prompt from the [quick start](QUICK-START.md), naming the handle explicitly on the first probe.
6. Repeat the upload only for additional handles you actually need.

## Expected success

- Claude accepts the selected ZIP without a structure error.
- The imported Skill is listed by the host.
- A fresh chat can invoke the named capability.

## Recovery

1. If upload is unavailable, stop: this package is statically valid but not installed on that host.
2. If the ZIP is rejected, verify its exact filename and SHA-256 through [validation](VALIDATION.md); do not repair it by recompressing.
3. If import succeeds but selection fails, name the handle explicitly once. Treat continued failure as a routing or runtime issue and use [support](SUPPORT.md).


## Remove or roll back

1. In Claude's Skills manager, disable or remove each TestForge handle you imported.
2. Start a fresh chat and confirm the removed handle is no longer listed or selected.
3. To roll back, upload the retained older ZIP for that handle unchanged and verify the displayed version before use.

Removing a Skill does not delete prior chats or verification artifacts outside the Skill package.
