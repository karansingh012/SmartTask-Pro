from __future__ import annotations

from typing import Any, Dict, Iterable

import numpy as np
import pandas as pd

from ..models import Task


def _to_dataframe(tasks: Iterable[Task]) -> pd.DataFrame:
    rows = [
        {
            "id": task.id,
            "status": (task.status or "pending").strip().lower(),
        }
        for task in tasks
    ]
    return pd.DataFrame(rows, columns=["id", "status"])


def build_task_analytics(tasks: Iterable[Task]) -> Dict[str, Any]:
    frame = _to_dataframe(tasks)
    if frame.empty:
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "completion_percentage": 0.0,
        }

    total_tasks = int(frame["id"].count())
    completed_tasks = int((frame["status"] == "completed").sum())
    pending_tasks = total_tasks - completed_tasks

    completion_percentage = float(
        np.round((completed_tasks / total_tasks) * 100, 2)
    )

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completion_percentage": completion_percentage,
    }


def get_user_task_analytics(user_id: int) -> Dict[str, Any]:
    tasks = Task.query.filter_by(user_id=user_id).all()
    return build_task_analytics(tasks)
