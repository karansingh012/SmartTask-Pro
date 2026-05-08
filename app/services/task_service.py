from ..models import Task


def list_tasks():
    return Task.query.order_by(Task.id.asc()).all()
