from __future__ import annotations

from typing import Any, Dict, Optional

from flask import Blueprint, current_app, jsonify, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from ..db import db
from ..models import Task
from ..websocket import socketio
from app.socketio import socketio


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


ALLOWED_STATUSES = {"pending", "in_progress", "completed", "archived"}


def _bad_request(message: str):
    return jsonify(error=message), 400


def _not_found():
    return jsonify(error="task not found"), 404


def _parse_task_payload(payload: Optional[Dict[str, Any]], *, partial: bool = False):
    if payload is None:
        return None, _bad_request("Missing JSON body")

    title = payload.get("title")
    description = payload.get("description")
    priority = payload.get("priority")
    status = payload.get("status")

    if isinstance(priority, str) and priority.isdigit():
        priority = int(priority)

    PRIORITY_MAP = {
        "low": 1,
        "normal": 3,
        "medium": 3,
        "high": 5,
    }

    if isinstance(priority, str) and priority.lower() in PRIORITY_MAP:
        priority = PRIORITY_MAP[priority.lower()]

    if not partial:
        if not isinstance(title, str) or not title.strip():
            return None, _bad_request("title is required")

    if title is not None and (not isinstance(title, str) or not title.strip()):
        return None, _bad_request("title must be a non-empty string")

    if description is not None and not isinstance(description, str):
        return None, _bad_request("description must be a string")

    if priority is not None:
        if not isinstance(priority, int) or not (1 <= priority <= 5):
            return None, _bad_request("priority must be an integer between 1 and 5")

    if isinstance(status, str):
        status = status.lower()

    if status is not None and status not in ALLOWED_STATUSES:
        return None, _bad_request("status is invalid")

    return {
        "title": title.strip() if isinstance(title, str) else None,
        "description": description,
        "priority": priority,
        "status": status,
    }, None


def _get_task(task_id: int) -> Optional[Task]:
    return Task.query.filter_by(id=task_id, user_id=current_user.id).first()


@tasks_bp.route("", methods=["GET"])
@login_required
def list_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.id.asc()).all()
    return jsonify(items=[task.to_dict() for task in tasks]), 200


@tasks_bp.route("/<int:task_id>", methods=["GET"])
@login_required
def get_task(task_id: int):
    task = _get_task(task_id)
    if not task:
        return _not_found()
    return jsonify(task=task.to_dict()), 200


@tasks_bp.route("", methods=["POST"])
@login_required
def create_task():
    payload_source = request.form.to_dict() or request.get_json(silent=True)

    payload, error = _parse_task_payload(payload_source)
    if error:
        return error

    task = Task(
        title=payload["title"],
        description=payload.get("description"),
        priority=payload.get("priority") or 3,
        status=payload.get("status") or "pending",
        user_id=current_user.id,
    )

    try:
        db.session.add(task)
        db.session.commit()
        socketio.emit("task_updated", {

             "action": "created"

        })
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Failed to create task")
        return jsonify(error="Unable to create task"), 500

    current_app.logger.info("Task created", extra={"task_id": task.id})
    socketio.emit(
        "task_created",
        {"task": task.to_dict(), "user_id": current_user.id},
    )
    return redirect(url_for("main.dashboard"))


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id: int):
    task = _get_task(task_id)
    if not task:
        return _not_found()

    payload, error = _parse_task_payload(
        request.get_json(silent=True), partial=True
    )
    if error:
        return error

    if payload["title"] is not None:
        task.title = payload["title"]
    if payload["description"] is not None:
        task.description = payload["description"]
    if payload["priority"] is not None:
        task.priority = payload["priority"]
    if payload["status"] is not None:
        task.status = payload["status"]

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Failed to update task")
        return jsonify(error="Unable to update task"), 500

    current_app.logger.info("Task updated", extra={"task_id": task.id})
    socketio.emit(
        "task_updated",
        {"task": task.to_dict(), "user_id": current_user.id},
    )
    return jsonify(task=task.to_dict()), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id: int):
    task = _get_task(task_id)
    if not task:
        return _not_found()

    try:
        db.session.delete(task)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Failed to delete task")
        return jsonify(error="Unable to delete task"), 500

    current_app.logger.info("Task deleted", extra={"task_id": task.id})
    return jsonify(message="task deleted"), 200


@tasks_bp.route("/<int:task_id>/complete", methods=["POST"])
@login_required
def complete_task(task_id: int):
    task = _get_task(task_id)
    if not task:
        return _not_found()

    task.status = "completed"

    current_app.logger.info(
        "Completing task",
        extra={"task_id": task.id, "user_id": current_user.id},
    )

    try:
        db.session.add(task)
        db.session.commit()
        db.session.refresh(task)
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Failed to complete task")
        return jsonify(error="Unable to complete task"), 500

    socketio.emit(
        "task_updated",
        {"task": task.to_dict(), "user_id": current_user.id},
    )

    return redirect(url_for("main.dashboard"))


@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task_form(task_id: int):
    task = _get_task(task_id)
    if not task:
        return _not_found()

    deleted_task_id = task.id

    try:
        db.session.delete(task)
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Failed to delete task")
        return jsonify(error="Unable to delete task"), 500

    socketio.emit(
        "task_deleted",
        {
            "task_id": deleted_task_id,
            "user_id": current_user.id,
        },
    )

    return redirect(url_for("main.dashboard"))
