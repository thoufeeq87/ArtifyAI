from fastapi import APIRouter, HTTPException
from celery import Celery
from celery.result import AsyncResult
from artify_common import settings
from .schemas import EnqueueRequest, TaskStatusResponse

router = APIRouter()
celery_client = Celery("artify", broker=settings.broker_url, backend=settings.result_backend)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/tasks/enqueue", response_model=TaskStatusResponse)
def enqueue(req: EnqueueRequest) -> TaskStatusResponse:
    task_name = f"worker.tasks.{req.type}"
    try:
        async_result = celery_client.send_task(task_name, kwargs=req.params, queue=req.queue)
        return TaskStatusResponse(task_id=async_result.id, status="PENDING", result=None)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
def task_status(task_id: str) -> TaskStatusResponse:
    res: AsyncResult = celery_client.AsyncResult(task_id)
    payload: dict = {"task_id": task_id, "status": res.status}
    if res.successful():
        payload["result"] = res.result
    elif res.failed():
        payload["result"] = str(res.result)
    return TaskStatusResponse(**payload)
