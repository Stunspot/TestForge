# TestForge: validation and evidence boundary

## Run the portable verifier

1. Open a terminal at the extracted release root.
2. Run:

   ```text
   python tools/verify_release.py .
   ```

3. Require exit code `0`, `"ok": true`, and an empty findings list.
4. Compare the result with [verification-report.json](../verification-report.json).

The verifier checks manifest-to-Codex byte parity, Claude ZIP hashes and members, ZIP path safety, plugin metadata, the documentation set, and private-topology leakage.

## Check the canonical archive

From the unextracted staging or download directory in PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 '.\TestForge-v1.1.3.zip'
Get-Content '.\TestForge-v1.1.3.zip.sha256'
```

The computed digest must match the detached checksum and the release receipt supplied beside the archive.

## What this proves

- Static source-record, Codex payload, and Claude archive parity.
- Declared exclusions and deterministic ZIP membership.
- Canonical-to-backup copy parity when the detached estate receipt records both files.

## What this does not prove

- Installation or host discovery.
- Invocation, routing quality, or healthy live tools.
- External publication or first customer value.

Record those states separately. See the [host evidence boundary](HOST-EVIDENCE-BOUNDARY.md) and [support procedure](SUPPORT.md).
