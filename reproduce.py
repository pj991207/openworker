"""Capture a real local-shell completion with a scripted (offline) model provider."""
import asyncio
import json
import os
from pathlib import Path
import sys
import tempfile

root = Path(sys.argv[1])
sys.path[:0] = [str(root), str(root / "tests")]
from coworker.server.manager import SessionManager
from coworker.sessions import SessionRecord
from test_engine import ScriptedProvider, _text_turn, _tool_turn


async def main():
    with tempfile.TemporaryDirectory(prefix="wake-demo-", ignore_cleanup_errors=True) as temp:
        folder = Path(temp)
        os.environ["COWORKER_STATE_DIR"] = str(folder / "state")
        os.environ["COWORKER_SCRATCH_BASE"] = str(folder / "scratch")
        workspace = folder / "workspace"
        workspace.mkdir()
        manager = SessionManager(data_dir=folder / "data", workspace=workspace,
                                 provider=ScriptedProvider([]))
        manager._maybe_autotitle = lambda *args: None
        manager.session_store.save(SessionRecord(session_id="demo", workspace=str(workspace),
                                                 model="gpt-5.5", mode="auto", agent="cowork"))
        engine = manager.get_engine("demo")
        started = engine.executor.run_background('Start-Sleep -Milliseconds 1500; Write-Output "BUILD_OK"')
        job = started["task_id"]
        engine.provider = ScriptedProvider([
            _tool_turn("shell_task_output", {"task_id": job}),
            _text_turn("Background build finished: BUILD_OK."),
        ])
        print("Provider: scripted/offline; execution: real Windows local shell", flush=True)
        print("Task started: " + job, flush=True)
        await manager.resume_due_wakes()
        print("Completion watches after first tick: " + str(len(manager.wakes.pending("demo"))), flush=True)
        task = engine.executor._bg_tasks[job]
        await asyncio.to_thread(task.proc.wait, 10)
        await asyncio.to_thread(task._reader.join, 10)
        assert task.proc.returncode == 0
        captured = "".join(task._lines).strip()
        assert captured == "BUILD_OK", captured
        print("Process exited; final output drained: " + captured, flush=True)
        resumed = await manager.resume_due_wakes()
        print("Sessions resumed after completion: " + str(resumed), flush=True)
        async def wait():
            while manager._team_inflight or manager.is_running("demo"):
                await asyncio.sleep(0.01)
        await asyncio.wait_for(wait(), timeout=30)
        messages = manager.session_store.load("demo").messages
        if resumed:
            assert any(m["role"] == "tool" and "BUILD_OK" in str(m.get("content", "")) for m in messages), messages
            print("Resumed agent read BUILD_OK through shell_task_output", flush=True)
        assistants = [m["content"] for m in messages if m["role"] == "assistant" and m.get("content")]
        print("Assistant reply: " + (assistants[-1] if assistants else "(none)"), flush=True)
        print("Extra resumes on next tick: " + str(await manager.resume_due_wakes()), flush=True)
        await manager.aclose()

asyncio.run(main())
