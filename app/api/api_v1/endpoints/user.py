from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.worker import celery

router = APIRouter()


@router.post("/update", status_code=201)
def read_users():
    task = celery.send_task("app.core.worker.update_data")
    print(task)
    return JSONResponse({"task_id": task.id})


@router.get("/update/{task_id}")
def get_update_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }

    return JSONResponse(result)
