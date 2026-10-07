from pathlib import Path
import copy,io,json,os,subprocess,sys,tempfile,unittest,zipfile
from unittest.mock import patch
from types import SimpleNamespace
from test_estate_quality import evidence,ROOT,SCRIPTS
from validate_manifest import validate
from validate_traceability import validate as trace
from assemble_report import assemble
from normalize_test_results import normalize
from archive_paths import check_members
import build_public_release
from build_public_release import zip_tree
from rebuild_public_release import write_zip

def residual(test_id="T-002"):
 return {"id":"RR-001","statement":"Optional display matrix remains unexercised","treatment":"Narrow claim excludes additional display variants","owner":"Product owner","revisit_condition":"Before expanding display support","test_ids":[test_id]}
def optional(d,critical=False):
 d["tests"].append({"id":"T-002","scenario_ids":["S-001"],"status":"unexecuted","decision_critical":critical})
 d["decision"]["status"]="READY_WITH_RESIDUAL_RISK";d["residual_risks"]=[residual()]
def support_recovery():
 d=evidence();old=copy.deepcopy(d["executions"][0]);old.update(id="E-000",status="failed",exit_code=2,superseded_by="E-001",triage_finding_id="F-001",raw_evidence="failed-support.log")
 old["test_ids"]=["T-001"];d["executions"][0]["test_ids"]=["T-001"]
 d["executions"].insert(0,old)
 d["findings"]=[{"id":"F-001","classification":"ENVIRONMENT_FAILURE","severity":"high","status":"resolved","statement":"Test interpreter unavailable in isolated shell; one explicit interpreter route succeeded","evidence":["failed-support.log","outcome.log"]}]
 return d

class DeeperEvidenceTests(unittest.TestCase):
 def test_candidate_bound_positive_control(self):self.assertTrue(validate(evidence())["valid"])
 def test_required_check_cannot_hide_in_residual(self):
  d=evidence();optional(d,True);self.assertFalse(validate(d)["valid"])
 def test_noncritical_omission_is_bounded_not_blanket_waiver(self):
  d=evidence();optional(d);self.assertTrue(validate(d)["valid"])
  d["residual_risks"][0]["test_ids"]=["other"];self.assertFalse(validate(d)["valid"])
 def test_nonapplicable_requires_real_scope_and_cannot_replace_required_check(self):
  d=evidence();d["tests"].append({"id":"T-002","scenario_ids":["S-001"],"status":"not_applicable"})
  self.assertFalse(validate(d)["valid"])
  d["tests"][-1]["applicability_reason"]="Mobile display is outside this server parser claim";self.assertTrue(validate(d)["valid"])
  d["tests"][-1]["decision_critical"]=True;self.assertFalse(validate(d)["valid"])
 def test_stale_execution_or_review_cannot_support_current_candidate(self):
  for section in ("executions","review"):
   d=evidence();row=d[section][0] if section=="executions" else d[section];row["target_revision"]="old"
   self.assertFalse(validate(d)["valid"])
 def test_ready_needs_identified_review_not_pass_word(self):
  d=evidence();d["review"]={"status":"REVIEW_PASS"};self.assertFalse(validate(d)["valid"])
 def test_reviewer_findings_need_disposition(self):
  d=evidence();d["review"]["findings"]=["Open persistence concern"];self.assertFalse(validate(d)["valid"])
  d["review"]["finding_dispositions"]={"Open persistence concern":{"status":"resolved","reason":"Current readback proves persistence"}};self.assertTrue(validate(d)["valid"])
 def test_blocking_review_condition_cannot_be_residualized(self):
  d=evidence();d["review"].update(status="REVIEW_PASS_WITH_CONDITIONS",conditions=[{"statement":"Restore validation must pass","status":"open","blocking":True}])
  d["decision"]["status"]="READY_WITH_RESIDUAL_RISK";d["residual_risks"]=[residual()]
  self.assertFalse(validate(d)["valid"])
  d["review"]["conditions"][0]["status"]="met";self.assertTrue(validate(d)["valid"])
 def test_actual_local_evidence_and_missing_file_control(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);d=evidence();self.assertFalse(validate(d,root)["valid"])
   (root/"outcome.log").write_text("Observed useful result");(root/"review.log").write_text("Reviewer inspected current result")
   self.assertTrue(validate(d,root)["valid"])
   d["executions"][0]["raw_evidence"]="../outside.log";self.assertFalse(validate(d,root)["valid"])
 def test_supplied_observation_does_not_fabricate_command(self):
  d=evidence();e=d["executions"][0];e.update(kind="observation",source="supplied",recorder="Named browser reviewer",procedure=["Enter at public home","Browse without a query"],observed=["Subject index leads to a readable source"],command=[],exit_code=None)
  self.assertTrue(validate(d)["valid"])
  e["command"]=["pretend-shell"];self.assertFalse(validate(d)["valid"])
 def test_proposed_observation_cannot_count_as_pass(self):
  d=evidence();d["executions"][0].update(kind="observation",command=[],exit_code=None,procedure=["Open site"],observed=[],source="observed",recorder="reviewer")
  self.assertFalse(validate(d)["valid"])
 def test_one_resolved_support_correction_preserves_failed_history(self):
  d=support_recovery();self.assertTrue(validate(d)["valid"])
  text=assemble(d);self.assertIn("failed-support.log",text);self.assertIn("ENVIRONMENT_FAILURE",text)
 def test_same_check_recovery_allows_changed_interpreter(self):
  d=support_recovery();d["executions"][1]["command"]=["explicit-python","outcome.py"]
  self.assertTrue(validate(d)["valid"])
 def test_support_recovery_scope_cannot_be_inferred(self):
  for which in (0,1):
   d=support_recovery();d["executions"][which].pop("test_ids")
   self.assertFalse(validate(d)["valid"])
 def test_unrelated_check_cannot_recover_failed_check(self):
  d=support_recovery();d["tests"].append({"id":"T-health","scenario_ids":["S-001"],"status":"passed","execution_id":"E-001"})
  d["executions"][1]["test_ids"]=["T-health"];self.assertFalse(validate(d)["valid"])
 def test_recovery_must_cover_every_failed_check(self):
  d=support_recovery();d["tests"].append({"id":"T-restore","scenario_ids":["S-001"],"status":"passed","execution_id":"E-001"})
  d["executions"][0]["test_ids"].append("T-restore");self.assertFalse(validate(d)["valid"])
 def test_recovery_must_map_failed_check_to_replacement_result(self):
  d=support_recovery();third=copy.deepcopy(d["executions"][1]);third["id"]="E-002";d["executions"].append(third)
  d["tests"][0]["execution_id"]="E-002";self.assertFalse(validate(d)["valid"])
 def test_recovery_unknown_and_malformed_scope_controlled(self):
  for value in (["ghost"],[],[{}],None,["T-001","T-001"]):
   d=support_recovery();d["executions"][0]["test_ids"]=value;self.assertFalse(validate(d)["valid"])
 def test_product_defect_is_not_support_recovery(self):
  d=support_recovery();d["findings"][0]["classification"]="PRODUCT_DEFECT";self.assertFalse(validate(d)["valid"])
 def test_two_support_corrections_exceed_cycle(self):
  d=support_recovery();extra=copy.deepcopy(d["executions"][0]);extra["id"]="E-099";d["executions"].append(extra);self.assertFalse(validate(d)["valid"])
 def test_final_report_preserves_all_decision_changing_qualifiers(self):
  d=evidence();d["claim_custody"]["assumed"]=[{"id":"A-1","statement":"Offline source snapshot assumed complete","basis":"Supplied by owner"}]
  d["claim_custody"]["unresolved"]=[{"id":"U-1","statement":"Future remote host not exercised","basis":"Outside narrow local scope"}]
  d["scope"]["excluded"]=["Remote provider behavior"];d["decision"]["authority_required"]=["Public upload still requires owner instruction"]
  text=assemble(d)
  for phrase in ("Offline source snapshot","Future remote host","Remote provider","Public upload","independent-fixture","does not grant release","persisted result"):
   self.assertIn(phrase,text)
 def test_technical_pass_does_not_grant_outstanding_release_authority(self):
  d=evidence();d["decision"]["authority_required"]=["Authorize a public upload"];self.assertTrue(validate(d)["valid"])
  d["decision"]["claims_release_authorization"]=True;self.assertFalse(validate(d)["valid"])
 def test_malformed_nested_records_controlled(self):
  mutations=[lambda d:d["executions"][0].update(status={}),lambda d:d["tests"][0].update(execution_id={}),lambda d:d["decision"].update(status=[]),lambda d:d["review"].update(status=[]),lambda d:d["risks"][0].update(severity={}),lambda d:d["review"].update(conditions=[{}]),lambda d:d["findings"].append({"severity":"high"})]
  for mutate in mutations:
   d=evidence();mutate(d);self.assertFalse(validate(d)["valid"])
 def test_generic_summary_cannot_erase_skipped_unknown_or_failed_cases(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)/"results.json"
   for case_status,expected in (("skipped","unparsed"),("unknown","unparsed"),("failed","failed"),("passed","passed")):
    p.write_text(json.dumps({"summary":{"total":1,"passed":1,"failed":0,"skipped":0,"errors":0,"status":"passed"},"cases":[{"name":"case","status":case_status}]}))
    self.assertEqual(expected,normalize(p)["summary"]["status"])
 def test_empty_generic_aggregate_does_not_establish_cases(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)/"results.json";p.write_text(json.dumps({"summary":{"total":1,"passed":1,"failed":0,"skipped":0,"errors":0,"status":"passed"}}));self.assertEqual("unparsed",normalize(p)["summary"]["status"])

class PortableCustodyTests(unittest.TestCase):
 def test_file_directory_collisions_in_both_orders(self):
  for entries in ([("assets",b"x"),("assets/icon.png",b"x")],[("assets/icon.png",b"x"),("ASSETS",b"x")]):
   with self.assertRaises(ValueError):check_members(entries)
 def test_explicit_directory_and_child_are_legitimate(self):
  check_members([("assets/",b""),("assets/icon.png",b"x")])
  check_members([("assets/icon.png",b"x"),("assets/",b"")])
 def test_nested_archive_collision_refused(self):
  b=io.BytesIO()
  with zipfile.ZipFile(b,"w") as z:z.writestr("assets","x");z.writestr("assets/icon.png","x")
  with self.assertRaises(ValueError):check_members([("nested.zip",b.getvalue())])
 def test_final_builder_never_deletes_accepted_directory(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);out=root/"releases/v2.0.0";out.mkdir(parents=True);(out/"accepted.txt").write_text("accepted")
   with patch.object(build_public_release,"ROOT",root),patch.object(build_public_release,"OUT",out),patch.object(build_public_release,"require_final_seal",return_value=SimpleNamespace(output_dir=None)):
    with self.assertRaises(RuntimeError):build_public_release.main([])
   self.assertEqual("accepted",(out/"accepted.txt").read_text())
 def test_source_junction_rejected_before_prior_archive_changes(self):
  if os.name!="nt":self.skipTest("Windows junction probe")
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);outside=root/"outside";outside.mkdir();(outside/"payload.txt").write_text("outside lexical owner")
   link=root/"link";cmd="New-Item -ItemType Junction -Path '"+str(link).replace("'","''")+"' -Target '"+str(outside).replace("'","''")+"' | Out-Null"
   result=subprocess.run(["powershell","-NoProfile","-Command",cmd],capture_output=True,text=True)
   if result.returncode:self.skipTest("junction creation unavailable")
   try:
    output=root/"prior.zip";output.write_bytes(b"prior accepted bytes")
    for builder in (lambda:zip_tree(link,output),lambda:write_zip(link,output,"root")):
     with self.assertRaises(ValueError):builder()
     self.assertEqual(b"prior accepted bytes",output.read_bytes())
   finally:os.rmdir(link)

if __name__=="__main__":unittest.main()