from flask import Flask, render_template, request
import json
import urllib.parse
import urllib.request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def details():
    if request.method == "GET":
        return render_template("inder.html")

    location = request.form.get("location", "").strip()
    if not location:
        return render_template("index.html", error="Give the correct location")

    try:
        q = urllib.parse.quote(location)

        # Free working endpoint (no key): photon (komoot)
        url = f"https://photon.komoot.io/api/?q={q}&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "FlaskGeocoder/1.0"})

        source = urllib.request.urlopen(req).read()
        responsedata = json.loads(source)

        feature = responsedata.get("features", []) 
        if not feature:
            return render_template("index.html", error="Give the correct location")

        # Photon returns [longitude, latitude]
        lon, lat = feature[0]["geometry"]["coordinates"]

        data = {
            "latitude": str(lat),
            "longitude": str(lon),
        }

        return render_template("index.html", data=data)

    except Exception:
        return render_template("index.html", error="Give the correct location")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)