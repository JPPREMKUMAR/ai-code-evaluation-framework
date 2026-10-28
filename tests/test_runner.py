import pytest
from app.runner import evaluate_candidate,run_candidate
from app import main,storage
from app.models import CodeReview

def test_reference_passes_all_cases():
    result=evaluate_candidate("merge-intervals","reference")
    assert result["test_count"]==7
    assert result["passed_count"]==7

def test_boundary_mutant_is_caught():
    result=evaluate_candidate("merge-intervals","misses-touching")
    boundary=next(r for r in result["results"] if r["case_id"]=="touching-boundary")
    assert boundary["passed"] is False

def test_empty_input_mutant_is_caught():
    result=evaluate_candidate("merge-intervals","crashes-empty")
    empty=next(r for r in result["results"] if r["case_id"]=="empty")
    assert empty["passed"] is False

def test_arbitrary_candidate_id_is_rejected():
    with pytest.raises(ValueError,match="allowlist"):
        run_candidate("merge-intervals","__import__('os').system('echo unsafe')",[])

def test_timeout_is_reported():
    result=run_candidate("merge-intervals","reference",[[1,2]],timeout_seconds=0.0001)
    assert result["status"]=="timeout"

def test_unknown_problem_rejected():
    with pytest.raises(KeyError):
        run_candidate("unknown","reference",[])

def test_review_scores_are_saved_with_report():
    report=evaluate_candidate("merge-intervals","reference")
    run_id=storage.save(report)
    review=CodeReview(correctness=5,edge_cases=5,complexity=4,readability=4,specification_adherence=5,rationale="The implementation follows the stated interval behavior and covers the edge cases.")
    assert main.save_review(run_id,review)["saved"] is True
    from app.main import json_report
    assert json_report(run_id)["human_review"]["complexity"]==4
    assert json_report(run_id)["run_id"]==run_id
