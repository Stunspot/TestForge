from pathlib import Path
import ast,copy,hashlib,importlib.util,json,subprocess,sys
ROOT=Path(r"E:\Github\testforge")
AUDIT=Path(r"E:\Indranet\Nova\projects\project-records\projects\augment-estate-quality-repair\records\product-audits\testforge")
EV=ROOT/"verification/shared-async-revisit"
EX=EV/"native-extract/testforge-v2.0.0"
SCRIPTS=EX/"codex/testforge/skills/software-verification/scripts"
sys.path.insert(0,str(SCRIPTS))
from validate_manifest import validate
from assemble_report import assemble
from normalize_test_results import normalize
def save(p,d):p.write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8",newline="\n")
tree=ast.parse((ROOT/"tests/test_estate_quality.py").read_text(encoding="utf-8"))
func=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="evidence")
ns={};exec(compile(ast.Module(body=[func],type_ignores=[]),"<retained-fixture>","exec"),ns)
evidence=ns["evidence"]
smoke=EV/"packaged-smoke";smoke.mkdir(exist_ok=True)
(smoke/"outcome.log").write_text("Synthetic retained evidence fixture: subject browsing completed.\n",encoding="utf-8")
(smoke/"review.log").write_text("Synthetic independent fixture record: current revision inspected.\n",encoding="utf-8")
checks=[]
def record(name,ok,detail):
 checks.append({"id":name,"passed":bool(ok),"observation":detail})
 if not ok: raise AssertionError(name)
d=evidence();r=validate(d,smoke);record("candidate-bound-positive-control",r["valid"],r)
d=evidence();d["tests"].append({"id":"T-002","scenario_ids":["S-001"],"status":"unexecuted","decision_critical":True})
d["decision"]["status"]="READY_WITH_RESIDUAL_RISK";d["residual_risks"]=[{"id":"RR-1","statement":"Missing required restore check","treatment":"Deferred","owner":"owner","revisit_condition":"Later","test_ids":["T-002"]}]
r=validate(d,smoke);record("required-evidence-cannot-be-waived",not r["valid"],r)
d=evidence();d["executions"][0].update(kind="observation",command=[],exit_code=None,source="supplied",recorder="Named browser observer",procedure=["Browse by subject without typing a query"],observed=["Reached readable source from subject index"])
r=validate(d,smoke);record("real-observation-without-fake-command",r["valid"],r)
d["claim_custody"]["unresolved"]=[{"id":"U-1","statement":"Future remote host not exercised","basis":"Outside local claim"}]
report=assemble(d,smoke);(smoke/"report.md").write_text(report,encoding="utf-8")
record("report-retains-source-and-limits",all(x in report for x in ("supplied","Future remote host","persisted result","does not grant release")),{"report":str(smoke/"report.md")})
p=smoke/"contradictory-results.json";save(p,{"summary":{"total":1,"passed":1,"failed":0,"skipped":0,"errors":0,"status":"passed"},"cases":[{"name":"required","status":"skipped"}]})
r=normalize(p);record("skipped-case-cannot-be-normalized-to-pass",r["summary"]["status"]=="unparsed",r)
d=evidence();d["executions"][0]["status"]={};r=validate(d,smoke);record("malformed-status-controlled",not r["valid"],r)
candidate=json.loads((EV/"candidate.json").read_text(encoding="utf-8"))
actual=hashlib.sha256(Path(candidate["candidate_zip"]).read_bytes()).hexdigest()
assert actual==candidate["sha256"]
save(EV/"packaged-runtime-smoke.json",{"candidate":candidate,"module_path":str(SCRIPTS),"synthetic_fixture_boundary":"Checks shipped deterministic semantics; these fixtures are not actual customer usage or independent review.","checks":checks,"ok":all(c["passed"] for c in checks)})
print(json.dumps({"ok":True,"checks":len(checks),"candidate_sha256":actual}))
