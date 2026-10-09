from dataclasses import replace
import shutil
import sys
import pytest
from syntaxlab.checks import check
from syntaxlab.runner import Result, checkpoint, run


def test_runner_capture_environment_stdin_cwd_and_status(tmp_path):
    result = run([sys.executable, "-c", "import os,sys; print(os.getcwd()); print(os.environ['LAB_TEST']); print(input()); print('diagnostic', file=sys.stderr); sys.exit(3)"],
                 tmp_path, env={"LAB_TEST": "configured"}, stdin="hello\n")
    assert result.code == 3 and not result.ok
    assert str(tmp_path) in result.stdout and "configured\nhello" in result.stdout
    assert "diagnostic" in result.stderr


def test_runner_missing_and_timeout(tmp_path):
    missing = run(["syntaxlab-nonexistent-tool-000"], tmp_path)
    assert missing.missing and missing.code == 127
    timed = run([sys.executable, "-c", "import time; print('before', flush=True); time.sleep(30)"], tmp_path, 1)
    assert timed.timed_out and "before" in timed.stdout and "Timed out" in timed.stderr


def test_arguments_are_not_shell_evaluated(tmp_path):
    result = run([sys.executable, "-c", "import sys; print(sys.argv[1])", "$(touch PWNED); hi"], tmp_path)
    assert result.ok and "$(touch PWNED)" in result.stdout
    assert not (tmp_path / "PWNED").exists()


def test_check_engine_records_failure_then_success(lab):
    e = lab.select("c-hello")
    path = lab.prepare(e)
    e = replace(e, checks=[{"type": "file", "path": "main.c"},
                           {"type": "command", "args": [sys.executable, "-c", "print('passed')"], "stdout": "passed"}])
    assert not check(e, path, lab.config, lab.progress)[0].passed
    assert e.id not in lab.progress.completed()
    (path / "main.c").write_text("student source")
    assert all(r.passed for r in check(e, path, lab.config, lab.progress))
    assert e.id in lab.progress.completed()


def test_check_stops_before_stale_binary(lab):
    e = lab.select("c-hello")
    path = lab.prepare(e)
    e = replace(e, checks=[{"type": "command", "args": [sys.executable, "-c", "raise SystemExit(1)"]},
                           {"type": "command", "args": [sys.executable, "-c", "open('stale','w').write('bad')"]}])
    results = check(e, path, lab.config, lab.progress)
    assert len(results) == 1 and not results[0].passed
    assert not (path / "stale").exists()


def test_infrastructure_is_distinct(lab):
    e = replace(lab.select("c-hello"), checks=[{"type": "command", "args": ["syntaxlab-no-tool"]}])
    path = lab.prepare(e)
    result = check(e, path, lab.config, lab.progress)[0]
    assert result.infrastructure and not result.passed


def test_missing_nested_compiler_is_infrastructure_error(lab):
    e = lab.select("c-hello")
    path = lab.prepare(e)
    (path / "main.c").write_text("int main(void) { return 0; }")
    results = check(e, path, replace(lab.config, cc="syntaxlab-missing-compiler"), lab.progress)
    assert results[-1].infrastructure and "syntaxlab-missing-compiler" in results[-1].output


@pytest.mark.skipif(not shutil.which("gcc"), reason="GCC is not installed")
@pytest.mark.parametrize("key", ["c-hello", "c-pointers-swap", "c-memory-realloc", "c-headers"])
def test_real_c_compilation_and_behavior(lab, key):
    e = lab.catalog.exercises[key]
    path = lab.workspaces.create(e)
    for name, text in e.solution.items():
        (path / name).write_text(text)
    results = check(e, path, lab.config, lab.progress)
    assert all(r.passed for r in results), results
    assert e.id in lab.progress.completed()


@pytest.mark.skipif(not shutil.which("gcc"), reason="GCC is not installed")
def test_real_compiler_diagnostics_preserved(lab):
    e = lab.select("c-hello")
    path = lab.prepare(e)
    (path / "main.c").write_text("int main(void) { syntax_error; }")
    results = check(e, path, lab.config, lab.progress)
    assert "syntax_error" in results[-1].output and "error:" in results[-1].output
    assert e.id not in lab.progress.completed()


@pytest.mark.parametrize("status", ["?? README.md\0", "M  projects/c/demo/main.c\0", " R projects/c/demo/x\0old\0"])
def test_git_checkpoint_refuses_unrelated_or_staged_changes(tmp_path, monkeypatch, status):
    calls = []
    def fake(args, cwd):
        calls.append(args)
        return Result(args, 0, status)
    monkeypatch.setattr("syntaxlab.runner.run", fake)
    result = checkpoint(tmp_path, tmp_path / "projects/c/demo", tmp_path / "data/progress.db", "checkpoint")
    assert not result.ok and "refused" in result.stderr
    assert len(calls) == 1


def test_git_checkpoint_scopes_stage_and_preserves_hook_failure(tmp_path, monkeypatch):
    calls = []
    def fake(args, cwd):
        calls.append(args)
        if args[1] == "status":
            return Result(args, 0, " M projects/c/demo/main.c\0 M data/progress.db\0")
        return Result(args, 1, stderr="hook rejected") if args[1] == "commit" else Result(args, 0)
    monkeypatch.setattr("syntaxlab.runner.run", fake)
    result = checkpoint(tmp_path, tmp_path / "projects/c/demo", tmp_path / "data/progress.db", "checkpoint")
    assert not result.ok and "hook rejected" in result.stderr
    assert ["git", "add", "--", "projects/c/demo", "data/progress.db"] in calls
    assert not any("--amend" in c or "--no-verify" in c for c in calls)
