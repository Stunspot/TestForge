# Limitations

- TestForge improves confidence; it cannot prove defect-freedom, security, reliability, or compliance.
- Model inspection is hypothesis generation and semantic review, not a sound static analyzer or compiler.
- Framework-compatible tests depend on accurate repository context and locally available target tooling.
- Passing tests establish only the behavior and environment they exercised. Coverage percentage does not establish risk coverage.
- The standard-library validator checks TestForge's required structure and semantics; it is not a complete general JSON Schema engine. Canonical JSON is always supported. Non-JSON YAML requires optional PyYAML.
- Result normalization supports JUnit XML, common Jest JSON, captured command records, and generic JSON. Framework variations may remain `unparsed` with raw evidence preserved.
- GitHub, CI, browser, API, issue-tracker, and external-system actions exist only when the host supplies and authorizes them.
- Fileless fallback cannot inspect, compile, execute, normalize, or validate. Its artifacts remain `UNEXECUTED`.
- Behavioral eval files are evaluator-guided episodes. Static validation of their structure is not evidence that a model passes them.
