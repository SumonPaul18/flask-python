from app import app
@app.route("/openstack")
def openstack():
    return render_template("dashboard.html")