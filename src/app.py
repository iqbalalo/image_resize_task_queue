import os
from flask import Flask, jsonify, request
import redis
from rq import Queue
from image_resize import resize_process

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Define RQ
r = redis.Redis(host="redis", port=6379, db=0)
q = Queue(connection=r)


@app.route('/resize', methods=["POST"])
def resize():
    """Upload image to resize
    Returns:
        json -- task_id
    """

    try:
        # Get file from request
        file = request.files['file']

        # Define file path
        if not file:
            return jsonify(dict(status="error", data="File not found!")), 400

        upload_file_path = "{}/uploads/{}".format(basedir, file.filename)

        # Save file in local to pass the path to job queue
        file.save(upload_file_path)

        # Enqueue the process
        task = q.enqueue(resize_process, upload_file_path)

        response_object = dict(
            status="success", data=dict(task_id=task.get_id()))

        return jsonify(response_object), 200
    except Exception as e:
        return jsonify(dict(status="error", data=e)), 500


@app.route("/resize/<string:task_id>", methods=["GET"])
def get_result(task_id):
    """Get result of particular task request

    Arguments:
        task_id {string} -- task_id should get from /resize API call

    Returns:
        json -- image base64 data
    """

    try:
        # Fetch the job from Queue
        task = q.fetch_job(task_id)

        if task:
            response_object = dict(status="success", data=task.result)

            # Task should deleted when it is fetched
            task.delete()
        else:
            response_object = dict(status="No task found")

        return jsonify(response_object), 200
    except Exception as e:
        return jsonify(dict(status="error", data=e)), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
