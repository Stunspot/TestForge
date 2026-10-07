from pathlib import Path
import json, sys, tempfile, unittest, importlib.util
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'plugins/testforge/skills/software-verification/scripts'
sys.path.insert(0,str(SCRIPTS))
from normalize_test_results import normalize
from validate_manifest import validate
from validate_traceability import validate as trace
sys.path.insert(0,str(ROOT/'tools'))
from archive_paths import check_members

def evidence():
 return {'manifest_version':'1.0','target':{'name':'real outcome','revision':'fixture-v1'},'scope':{'included':['user completes task']},'claim_custody':{x:[] for x in ('observed','inferred','assumed','unresolved')},'risks':[{'id':'R-001','severity':'high','disposition':'covered','verification':['T-001']}],'scenarios':[{'id':'S-001','risk_ids':['R-001'],'expected':['persisted result']}],'tests':[{'id':'T-001','scenario_ids':['S-001'],'status':'passed','execution_id':'E-001'}],'executions':[{'id':'E-001','status':'passed','exit_code':0,'command':['python','outcome.py'],'raw_evidence':'outcome.log','target_revision':'fixture-v1','environment':'isolated local test fixture'}],'findings':[],'residual_risks':[],'review':{'status':'REVIEW_PASS','reviewer':'independent-fixture','raw_evidence':'review.log','target_revision':'fixture-v1','evidence_cutoff':'after fixture run','findings':[]},'decision':{'status':'READY','basis':['persisted outcome observed']}}

class EvidenceRegressions(unittest.TestCase):
 def xml(self,text):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'result.xml'; p.write_text(text); return normalize(p)
 def test_missing_aggregate_failure_is_failure(self):
  r=self.xml('<testsuite><testcase name="bad"><failure>broken</failure></testcase></testsuite>')
  self.assertEqual(('failed',1,0),(r['summary']['status'],r['summary']['failed'],r['summary']['passed']))
 def test_nested_namespaced_counts_once(self):
  r=self.xml('<testsuites xmlns="urn:junit"><testsuite tests="1"><testsuite tests="1"><testcase name="ok"/></testsuite></testsuite></testsuites>')
  self.assertEqual((1,'passed'),(r['summary']['total'],r['summary']['status']))
 def test_empty_and_skipped_are_not_pass(self):
  self.assertEqual('unparsed',self.xml('<testsuite tests="0"/>')['summary']['status'])
  self.assertEqual('unparsed',self.xml('<testsuite><testcase><skipped/></testcase></testsuite>')['summary']['status'])
 def test_aggregate_failure_cannot_be_erased(self):
  self.assertEqual('unparsed',self.xml('<testsuite failures="1"><testcase/></testsuite>')['summary']['status'])
 def test_wrong_xml_is_not_a_test_run(self):
  with self.assertRaises(ValueError): self.xml('<html/>')
 def test_json_unsupported_and_contradictory_are_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'result.json'
   for data in ([],{}, {'command':['test'],'status':'passed','exit_code':1},{'numTotalTests':2,'numPassedTests':3}):
    p.write_text(json.dumps(data))
    with self.assertRaises(ValueError): normalize(p)
 def test_valid_complete_chain_passes(self): self.assertTrue(validate(evidence())['valid'])
 def test_empty_ready_is_rejected(self):
  d=evidence()
  for k in ('risks','scenarios','tests','executions'): d[k]=[]
  self.assertFalse(validate(d)['valid'])
 def test_open_defect_exit_mismatch_and_no_raw_evidence(self):
  for mutate in (lambda d:d['findings'].append({'id':'F-001','classification':'PRODUCT_DEFECT','severity':'high','status':'open'}),lambda d:d['executions'][0].update(exit_code=1),lambda d:d['executions'][0].pop('raw_evidence')):
   d=evidence();mutate(d);self.assertFalse(validate(d)['valid'])
 def test_invalid_shapes_and_links_return_errors(self):
  for d in ([],{'tests':None},{'risks':[{'id':'R'},{'id':'R'}]}, {'scenarios':[{'id':'S','risk_ids':['ghost'],'expected':['x']}]}):
   self.assertFalse(trace(d)['valid'])
 def test_passing_test_cannot_use_unparsed_execution(self):
  d=evidence();d['executions'][0]['status']='unparsed';self.assertFalse(validate(d)['valid'])
 def test_portable_member_rejections(self):
  for entries in ([('A.txt',b''),('a.txt',b'')],[('x/'+'a'*190+'.txt',b'')],[('CON.txt',b'')],[('../escape',b'')]):
   with self.assertRaises(ValueError): check_members(entries)

 def test_ready_cannot_mean_all_work_unexecuted(self):
  d=evidence();d["risks"][0].update(severity="low",disposition="planned")
  d["tests"][0]["status"]="unexecuted";d["executions"][0]["status"]="not_run"
  self.assertFalse(validate(d)["valid"])
 def test_partial_ready_requires_qualified_residual_risk(self):
  d=evidence();d["tests"].append({"id":"T-002","scenario_ids":["S-001"],"status":"unexecuted","decision_critical":False})
  self.assertFalse(validate(d)["valid"])
  d["decision"]["status"]="READY_WITH_RESIDUAL_RISK";d["residual_risks"]=[{"id":"RR-001","statement":"T-002 remains unexecuted","treatment":"Outside the required narrow claim","owner":"fixture owner","revisit_condition":"Before broader release","test_ids":["T-002"]}]
  self.assertTrue(validate(d)["valid"])
 def test_malformed_trace_links_do_not_crash(self):
  for section,field in (("tests","scenario_ids"),("scenarios","risk_ids"),("risks","verification")):
   for value in ([{}],[[]],{},None):
    d=evidence();d[section][0][field]=value
    self.assertFalse(validate(d)["valid"])
 def test_jest_observed_failure_beats_aggregate_pass(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"result.json"
   p.write_text(json.dumps({"numTotalTests":1,"numPassedTests":1,"numFailedTests":0,"success":True,"testResults":[{"assertionResults":[{"title":"bad","status":"failed"}]}]}))
   result=normalize(p)
   self.assertEqual("failed",result["summary"]["status"]);self.assertEqual(1,result["summary"]["failed"]);self.assertTrue(result["parse_warnings"])
 def test_jest_no_cases_or_mismatch_cannot_pass(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"result.json"
   for suites in ([],[{"assertionResults":[{"status":"skipped"}]}]):
    p.write_text(json.dumps({"numTotalTests":1,"numPassedTests":1,"numFailedTests":0,"success":True,"testResults":suites}))
    self.assertEqual("unparsed",normalize(p)["summary"]["status"])

if __name__=='__main__': unittest.main()