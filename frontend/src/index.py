from flask import Flask, render_template, request, send_file
from pydantic import ValidationError
from simulation.simulation_service import findFileContentById, saveFileImage, findSimulationsByFile
from file.file import File
import httpx
import traceback

app = Flask(__name__)

# BACKEND_URL = "http://localhost:5000/"
BACKEND_URL = "http://backend/"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ping")
def ping():
    try:
        backend_url = BACKEND_URL + "database-ping/"
        response = httpx.get(backend_url)
        # Verificar si la respuesta es exitosa (código 200)
        if response.status_code == 200:
            try:
                data = (
                    response.json()
                )  # Intentar obtener el contenido JSON de la respuesta
                return render_template(
                    "index.html", ping_resp=data.get("message", "No message found")
                )
            except Exception as e:
                return render_template(
                    "index.html", ping_resp="Error decoding JSON response"
                )
        else:
            return render_template(
                "index.html",
                ping_resp=f"Unexpected status code: {response.status_code}. Response content: {response.text}",
            )
    except Exception as e:
        traceback_str = traceback.format_exc()
        return render_template("index.html", ping_resp=str(traceback_str))


@app.route("/files")
def files():
    try:
        backend_url = BACKEND_URL + "files/"
        response = httpx.get(backend_url)
        return render_template("files.html", files=response.json())
    except Exception as e:
        return render_template("files.html")


@app.route("/view/<file_id>")
def view_file(file_id):
    try:
        # Genera y guarda imagenes de simulaciones
        results = findSimulationsByFile(file_id)

        return render_template(
            "view-file.html", filename=file_id, results=results
        )
    except AttributeError as e:
        raise e  # Levanta la excepción original
    except Exception as e:
        traceback_str = traceback.format_exc()
        return render_template("index.html", alert=str(traceback_str))


@app.route("/view-map/<filename>")
def view_map(filename):
    dir = "/app/images/"
    return send_file(dir + filename + '.png', mimetype="image/png")


@app.route("/files/upload", methods=["GET", "POST"])
def upload_file():
    try:
        if request.method == "POST":
            backend_url = BACKEND_URL + "files/upload"

            name = request.form.get("name")
            content = request.files["file"]
            file_content = content.read()

            file_data = {"name": name, "content": file_content.decode("utf-8")}
            file = File(**file_data)

            if file:
                # Enviar el archivo al backend
                response = httpx.post(
                    backend_url,
                    json=file.dict(),
                    headers={"Content-Type": "application/json"},
                )
                return files()
            else:
                return "No se proporcionó ningún archivo"
        return render_template("upload-file.html")
    except Exception as e:
        traceback_str = traceback.format_exc()
        return render_template("index.html", ping_resp=str(traceback_str))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/simulate-file/<file_id>", methods=["GET", "POST"])
def simulate_file(file_id):

    if request.method == "POST":
        try:
            backend_url = BACKEND_URL + "simulate"
            # Parsea los datos del formulario y crea una instancia de la clase Simulation
            simulation_data = {
                "file_id": file_id,
                "model": request.form["model"],
                "windSpd": float(request.form["windSpd"]),
                "windDir": float(request.form["windDir"]),
                "start_time": float(request.form["start_time"]),
                "end_time": float(request.form["end_time"]),
            }

            # Enviar el archivo al backend
            response = httpx.post(
                backend_url,
                json=simulation_data,
                headers={"Content-Type": "application/json"},
            )
            return files()
        except ValidationError as e:
            render_template("files.html", alert=str(e))
        except Exception as e:
            render_template("files.html", alert=str(e))
    return render_template("simulate-file.html", file_id=file_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
