# Support and versioning

TestForge uses semantic versioning for package releases. Verification reports bind conclusions to the package version, target revision, environment, and evidence cutoff; upgrading TestForge does not retroactively change an old assessment.

Preserve the complete installed package when upgrading. Re-run package verification and reopen affected behavioral reviews when skill logic, status rules, schemas, deterministic parsing, or authority boundaries change materially.

Public defects and portability reports may be submitted through the [official TestForge issue tracker](https://github.com/Stunspot/TestForge/issues). Use a synthetic or sanitized reproduction and include the TestForge version, host, operating system, expected result, actual result, and exact error text. For a suspected vulnerability that cannot be safely disclosed in public, request a private route through [Collaborative Dynamics](https://collaborative-dynamics.com).

The free release carries no support SLA. Do not include secrets, customer data, unnecessary proprietary source, or active third-party exploit details in an issue.

## Upgrade from 1.1.7 to 2.0.0

The assessor no longer emits `plan_sha256`. Update JSON consumers to stop requiring that field; paid authority remains bound by the trusted dispatcher to the exact execution and complete canonical plan content. The major version acknowledges possible external caller breakage. Capacity arithmetic and authority boundaries are unchanged. See [2.0.0 release notes](../../RELEASE-NOTES-v2.0.0.md).
