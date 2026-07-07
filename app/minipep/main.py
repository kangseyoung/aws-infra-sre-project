import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse

from .database import connect, init_db
from .models import Equipment, EquipmentCreate, Job, JobCreate, JobUpdate
from .repository import (
    create_equipment,
    create_job,
    delete_job,
    list_equipment,
    list_jobs,
    update_job,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("minipep")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("MiniPEP database initialized")
    yield


app = FastAPI(title="MiniPEP", version="0.1.0", lifespan=lifespan)


@app.middleware("http")
async def request_logging(request: Request, call_next):
    started_at = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - started_at) * 1000
    logger.info(
        "request method=%s path=%s status=%s duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    with connect() as db:
        equipment = list_equipment(db)
        jobs = list_jobs(db)

    equipment_rows = "\n".join(
        f"""
        <tr>
          <td>{item["id"]}</td>
          <td>{escape(item["name"])}</td>
          <td>{escape(item["type"])}</td>
          <td>{escape(item.get("location") or "-")}</td>
          <td><span class="status">{escape(item["status"])}</span></td>
        </tr>
        """
        for item in equipment
    )
    job_rows = "\n".join(
        f"""
        <tr>
          <td>{job["id"]}</td>
          <td>{escape(job["title"])}</td>
          <td>{escape(job.get("equipment_name") or "-")}</td>
          <td>{escape(job["status"])}</td>
          <td>{escape(job["priority"])}</td>
        </tr>
        """
        for job in jobs[:8]
    )

    return f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>MiniPEP Dashboard</title>
        <style>
          :root {{
            --bg: #f4f6f8;
            --surface: #ffffff;
            --text: #1f2933;
            --muted: #5b6776;
            --line: #d9e2ec;
            --accent: #0f766e;
            --accent-soft: #ccfbf1;
          }}
          * {{ box-sizing: border-box; }}
          body {{
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            color: var(--text);
            background: var(--bg);
          }}
          header {{
            background: #17202a;
            color: #fff;
            padding: 24px;
          }}
          main {{
            width: min(1120px, calc(100% - 32px));
            margin: 24px auto 48px;
          }}
          h1, h2 {{ margin: 0; }}
          h1 {{ font-size: 2rem; }}
          h2 {{ font-size: 1.1rem; margin-bottom: 12px; }}
          p {{ color: var(--muted); line-height: 1.5; }}
          .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
          }}
          .metric, section {{
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 6px;
          }}
          .metric {{ padding: 16px; }}
          .metric strong {{ display: block; font-size: 1.8rem; }}
          section {{ padding: 16px; margin-top: 16px; overflow-x: auto; }}
          table {{ width: 100%; border-collapse: collapse; min-width: 620px; }}
          th, td {{
            border-bottom: 1px solid var(--line);
            padding: 10px 8px;
            text-align: left;
            font-size: 0.95rem;
          }}
          th {{ color: var(--muted); font-weight: 700; }}
          .links a {{
            display: inline-block;
            margin-right: 12px;
            color: var(--accent);
            font-weight: 700;
          }}
          .status {{
            background: var(--accent-soft);
            color: #115e59;
            border-radius: 999px;
            padding: 3px 8px;
            font-size: 0.85rem;
          }}
        </style>
      </head>
      <body>
        <header>
          <h1>MiniPEP</h1>
          <p>FastAPI demo app for EC2 Docker deployment behind an AWS ALB.</p>
        </header>
        <main>
          <div class="summary">
            <div class="metric"><span>Equipment</span><strong>{len(equipment)}</strong></div>
            <div class="metric"><span>Jobs</span><strong>{len(jobs)}</strong></div>
            <div class="metric"><span>Health</span><strong>OK</strong></div>
          </div>
          <p class="links">
            <a href="/health">/health</a>
            <a href="/api/equipment">/api/equipment</a>
            <a href="/api/jobs">/api/jobs</a>
            <a href="/docs">OpenAPI docs</a>
          </p>
          <section>
            <h2>Equipment</h2>
            <table>
              <thead><tr><th>ID</th><th>Name</th><th>Type</th><th>Location</th><th>Status</th></tr></thead>
              <tbody>{equipment_rows}</tbody>
            </table>
          </section>
          <section>
            <h2>Recent Jobs</h2>
            <table>
              <thead><tr><th>ID</th><th>Title</th><th>Equipment</th><th>Status</th><th>Priority</th></tr></thead>
              <tbody>{job_rows}</tbody>
            </table>
          </section>
        </main>
      </body>
    </html>
    """


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "minipep"}


@app.get("/api/equipment", response_model=list[Equipment])
def get_equipment_api() -> list[dict]:
    with connect() as db:
        return list_equipment(db)


@app.post("/api/equipment", response_model=Equipment, status_code=status.HTTP_201_CREATED)
def post_equipment_api(payload: EquipmentCreate) -> dict:
    with connect() as db:
        equipment = create_equipment(db, payload)
    logger.info("equipment_created id=%s name=%s", equipment["id"], equipment["name"])
    return equipment


@app.get("/api/jobs", response_model=list[Job])
def get_jobs_api() -> list[dict]:
    with connect() as db:
        jobs = list_jobs(db)
    return [{key: value for key, value in job.items() if key != "equipment_name"} for job in jobs]


@app.post("/api/jobs", response_model=Job, status_code=status.HTTP_201_CREATED)
def post_job_api(payload: JobCreate) -> dict:
    try:
        with connect() as db:
            job = create_job(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    logger.info("job_created id=%s title=%s", job["id"], job["title"])
    return job


@app.put("/api/jobs/{job_id}", response_model=Job)
def put_job_api(job_id: int, payload: JobUpdate) -> dict:
    try:
        with connect() as db:
            job = update_job(db, job_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"job_id {job_id} does not exist") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    logger.info("job_updated id=%s status=%s priority=%s", job["id"], job["status"], job["priority"])
    return job


@app.delete("/api/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_api(job_id: int) -> Response:
    try:
        with connect() as db:
            delete_job(db, job_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"job_id {job_id} does not exist") from exc
    logger.info("job_deleted id=%s", job_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )
