from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Temporary task storage
tasks = [
    {
        "id": 1,
        "task": "Complete CCD Assignment",
        "subject": "Cloud Computing",
        "deadline": "2026-09-25",
        "priority": "High",
        "status": "Pending"
    }
]


@app.route("/")
def home():
    filter_status = request.args.get("status", "All")
    search_query = request.args.get("search", "").strip().lower()
    sort_order = request.args.get("sort", "none")

    if filter_status == "Pending":
        filtered_tasks = [
            task for task in tasks if task["status"] == "Pending"
        ]
    elif filter_status == "Completed":
        filtered_tasks = [
            task for task in tasks if task["status"] == "Completed"
        ]
    elif filter_status == "High":
        filtered_tasks = [
            task for task in tasks if task["priority"] == "High"
        ]
    else:
        filtered_tasks = tasks.copy()

    # Search tasks by task name or subject
    if search_query:
        filtered_tasks = [
            task for task in filtered_tasks
            if search_query in task["task"].lower()
            or search_query in task["subject"].lower()
        ]

    # Sort tasks by deadline
    if sort_order == "earliest":
        filtered_tasks.sort(key=lambda task: task["deadline"])
    elif sort_order == "latest":
        filtered_tasks.sort(
            key=lambda task: task["deadline"],
            reverse=True
        )

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks if task["status"] == "Completed"
    )

    pending_tasks = sum(
        1 for task in tasks if task["status"] == "Pending"
    )

    high_priority_tasks = sum(
        1 for task in tasks if task["priority"] == "High"
    )

    return render_template(
        "index.html",
        tasks=filtered_tasks,
        current_filter=filter_status,
        search_query=search_query,
        sort_order=sort_order,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        high_priority_tasks=high_priority_tasks
    )


@app.route("/add-task", methods=["POST"])
def add_task():
    task_name = request.form.get("task", "")
    subject = request.form.get("subject", "")
    deadline = request.form.get("deadline", "")
    priority = request.form.get("priority", "")

    # Remove extra spaces from input
    task_name = task_name.strip()
    subject = subject.strip()
    deadline = deadline.strip()
    priority = priority.strip()

    # Validate required fields
    if not task_name:
        return "Task name cannot be empty or contain only spaces.", 400

    if not subject:
        return "Subject cannot be empty or contain only spaces.", 400

    if not deadline:
        return "Deadline is required.", 400

    if not priority:
        return "Priority is required.", 400

    # Validate priority
    valid_priorities = ["High", "Medium", "Low"]

    if priority not in valid_priorities:
        return "Invalid priority.", 400

    new_task = {
        "id": len(tasks) + 1,
        "task": task_name,
        "subject": subject,
        "deadline": deadline,
        "priority": priority,
        "status": "Pending"
    }

    tasks.append(new_task)

    return redirect(url_for("home"))


@app.route("/complete-task/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "Completed"
            break

    return redirect(url_for("home"))


@app.route("/delete-task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            break

    return redirect(url_for("home"))


@app.route("/api/tasks")
def api_tasks():
    return jsonify({
        "total_tasks": len(tasks),
        "tasks": tasks
    })


@app.route("/statistics")
def statistics():
    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks if task["status"] == "Completed"
    )

    pending_tasks = sum(
        1 for task in tasks if task["status"] == "Pending"
    )

    high_priority_tasks = sum(
        1 for task in tasks if task["priority"] == "High"
    )

    return jsonify({
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "high_priority_tasks": high_priority_tasks
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)