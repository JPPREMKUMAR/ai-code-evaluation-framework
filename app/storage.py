import json,os,sqlite3
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime,timezone
from dotenv import load_dotenv
load_dotenv()
DB_PATH=Path(os.getenv("DATABASE_PATH","./code-evaluations.db"))

@contextmanager
def db():
    DB_PATH.parent.mkdir(parents=True,exist_ok=True);c=sqlite3.connect(DB_PATH);c.row_factory=sqlite3.Row
    try:yield c;c.commit()
    except Exception:c.rollback();raise
    finally:c.close()

def initialize():
    with db() as c:c.execute("CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY AUTOINCREMENT,problem_id TEXT NOT NULL,candidate_id TEXT NOT NULL,report_json TEXT NOT NULL,created_at TEXT NOT NULL)")

def save(report):
    with db() as c:
        cur=c.execute("INSERT INTO runs(problem_id,candidate_id,report_json,created_at) VALUES(?,?,?,?)",(report["problem_id"],report["candidate_id"],json.dumps(report),datetime.now(timezone.utc).isoformat()))
        run_id=cur.lastrowid
        report["run_id"]=run_id
        c.execute("UPDATE runs SET report_json=? WHERE id=?",(json.dumps(report),run_id))
        return run_id

def history(limit=30):
    with db() as c:return [dict(r) for r in c.execute("SELECT id,problem_id,candidate_id,created_at,report_json FROM runs ORDER BY id DESC LIMIT ?",(limit,))]

def update_review(run_id:int,review:dict):
    with db() as c:
        row=c.execute("SELECT report_json FROM runs WHERE id=?",(run_id,)).fetchone()
        if not row:return False
        report=json.loads(row["report_json"]);report["human_review"]=review
        c.execute("UPDATE runs SET report_json=? WHERE id=?",(json.dumps(report),run_id))
    return True
