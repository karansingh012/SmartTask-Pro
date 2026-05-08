from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    tasks = current_user.tasks

    completed_tasks = [
        task
        for task in tasks
        if (task.status or "pending").strip().lower() == "completed"
    ]

    pending_tasks = [
        task
        for task in tasks
        if (task.status or "pending").strip().lower() == "pending"
    ]

    analytics = {
        "total_tasks": len(tasks),
        "completed_tasks": len(completed_tasks),
        "pending_tasks": len(pending_tasks),
        "completion_percentage": (
            round((len(completed_tasks) / len(tasks)) * 100, 2)
            if tasks
            else 0
        ),
    }

    return render_template(
        "dashboard.html",
        user=current_user,
        tasks=tasks,
        analytics=analytics,
    )