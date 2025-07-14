from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# JDoodle API credentials
CLIENT_ID = "a4572420c1ee2527c8ac13d4e78b39a9"
CLIENT_SECRET = "30307c1631fd1ef4645907bbe34cf1baabd95b4e3f5df8aefbcf6818fe4232d5"

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        code = request.form.get("code", "")
        language = request.form.get("language", "")
        version_index = get_version_index(language)

        payload = {
            "clientId": CLIENT_ID,
            "clientSecret": CLIENT_SECRET,
            "script": code,
            "language": language,
            "versionIndex": version_index
        }

        try:
            res = requests.post("https://api.jdoodle.com/v1/execute", json=payload)
            res.raise_for_status()
            data = res.json()
            output = data.get("output", "No output returned.")
        except requests.exceptions.RequestException as e:
            output = f"❌ Network error: {e}"
        except Exception as e:
            output = f"❌ Unexpected error: {e}"

    return render_template("index.html", output=output)

def get_version_index(language):
    return {
        "python3": "3",
        "java": "4",
        "c": "5",
        "cpp": "5",
        "php": "3",
        "ruby": "3",
        "go": "3",
        "javascript": "4",
        "swift": "3",
        "rust": "3",
        "kotlin": "2",
        "scala": "2",
        "perl": "3",
        "r": "3",
        "haskell": "3",
        "bash": "3",
        "sql": "3"  # ✅ JDoodle SQL version index
    }.get(language, "0")

if __name__ == "__main__":
    app.run(debug=True)
