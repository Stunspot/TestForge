# TestForge: support and recovery

## Support route

1. Search existing reports in the [repository issue tracker](https://github.com/Stunspot/TestForge/issues).
2. If you have repository access, open a new issue in the [repository issue tracker](https://github.com/Stunspot/TestForge/issues) and attach the [evidence bundle](#evidence-bundle).
3. If the repository is private and you do not have access, send the same bundle to the person or organization that supplied the package and ask them to escalate it to the repository maintainer.

Do not include credentials, private corpus content, customer data, or unrelated logs.

## Evidence bundle

- Family: `testforge`
- Version: `1.1.3`
- Intended handle
- Host name and host version
- Installation method and exact step that failed
- Expected result and observed result
- Output from `python tools/verify_release.py .`
- [manifest.json](../manifest.json)
- [verification-report.json](../verification-report.json)
- [description-custody.json](../description-custody.json)
- Whether failure occurs during packaging, installation, discovery, invocation, tool use, or output review

## Issue body

```text
Family and version:
Handle:
Host and version:
Installation method:
Expected result:
Observed result:
Static verifier result:
Reproduction steps:
Sensitive information removed: yes or no
```

## Recovery order

1. Establish static package integrity through [validation](VALIDATION.md).
2. Reinstall from the untouched canonical artifact.
3. Probe in a fresh task or chat with an explicit handle name.
4. Escalate with the bounded evidence bundle.
