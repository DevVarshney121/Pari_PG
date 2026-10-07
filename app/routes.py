import os
import re
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from .db import get_connection

site = Blueprint("site", __name__)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("site.admin_login"))
        return view(*args, **kwargs)
    return wrapped

def fetch_all(table, where="", params=()):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(f"SELECT * FROM {table} {where}", params)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

def fetch_one(table, row_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(f"SELECT * FROM {table} WHERE id=%s", (row_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    return row

@site.get("/")
def home():
    data = {
        "settings": fetch_one("settings", 1),
        "rooms": fetch_all("rooms", "WHERE active=1 ORDER BY sort_order, id"),
        "facilities": fetch_all("facilities", "WHERE active=1 ORDER BY sort_order, id"),
        "gallery": fetch_all("gallery", "WHERE active=1 ORDER BY sort_order, id"),
        "testimonials": fetch_all("testimonials", "WHERE active=1 ORDER BY sort_order, id"),
        "faqs": fetch_all("faqs", "WHERE active=1 ORDER BY sort_order, id"),
    }
    return render_template("index.html", **data)

@site.post("/api/contact")
def submit_contact():
    data = request.get_json(silent=True) or request.form
    name = str(data.get("name","")).strip()
    email = str(data.get("email","")).strip()
    phone = str(data.get("phone","")).strip()
    message = str(data.get("message","")).strip()

    if not name or not email or not phone or not message:
        return jsonify(success=False, message="Please fill all required fields."), 400
    if len(name)>100 or len(email)>150 or len(phone)>20 or len(message)>2000:
        return jsonify(success=False, message="One or more fields are too long."), 400
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify(success=False, message="Please enter a valid email address."), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contact_messages(name,email,phone,message) VALUES(%s,%s,%s,%s)",
        (name,email,phone,message)
    )
    conn.commit()
    cur.close(); conn.close()
    return jsonify(success=True, message="Thank you! Your message has been submitted successfully.")

@site.get("/api/rooms")
def api_rooms():
    return jsonify(fetch_all("rooms", "WHERE active=1 ORDER BY sort_order,id"))

@site.route("/admin/login", methods=["GET","POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("site.admin_dashboard"))
    error = None
    if request.method == "POST":
        if request.form.get("username","").strip() == ADMIN_USERNAME and request.form.get("password","") == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("site.admin_dashboard"))
        error = "Invalid username or password."
    return render_template("admin/login.html", error=error)

@site.get("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("site.admin_login"))

@site.get("/admin")
@site.get("/admin/")
@admin_required
def admin_dashboard():
    search = request.args.get("search","").strip()
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    like = f"%{search}%"
    if search:
        cur.execute("""SELECT * FROM contact_messages
                       WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s OR message LIKE %s
                       ORDER BY created_at DESC""", (like,like,like,like))
    else:
        cur.execute("SELECT * FROM contact_messages ORDER BY created_at DESC")
    messages = cur.fetchall()
    stats = {}
    for table in ["contact_messages","rooms","facilities","gallery","testimonials","faqs"]:
        cur.execute(f"SELECT COUNT(*) total FROM {table}")
        stats[table] = cur.fetchone()["total"]
    cur.close(); conn.close()
    return render_template("admin/dashboard.html", messages=messages, search=search, stats=stats)

@site.route("/admin/contact/edit/<int:message_id>", methods=["GET","POST"])
@admin_required
def contact_edit(message_id):
    if request.method == "POST":
        conn=get_connection(); cur=conn.cursor()
        cur.execute("""UPDATE contact_messages SET name=%s,email=%s,phone=%s,message=%s WHERE id=%s""",
                    (request.form["name"].strip(),request.form["email"].strip(),request.form["phone"].strip(),request.form["message"].strip(),message_id))
        conn.commit(); cur.close(); conn.close()
        flash("Contact submission updated.", "success")
        return redirect(url_for("site.admin_dashboard"))
    row=fetch_one("contact_messages", message_id)
    if not row: return "Not found",404
    return render_template("admin/contact_edit.html", row=row)

@site.post("/admin/contact/delete/<int:message_id>")
@admin_required
def contact_delete(message_id):
    conn=get_connection(); cur=conn.cursor()
    cur.execute("DELETE FROM contact_messages WHERE id=%s",(message_id,))
    conn.commit(); cur.close(); conn.close()
    flash("Contact submission deleted.", "success")
    return redirect(url_for("site.admin_dashboard"))

MODULES = {
    "rooms": {
        "title":"Rooms", "table":"rooms",
        "fields":["title","room_type","price","tag","image_url","description","beds","meta","features","available","active","sort_order"],
        "labels":{"title":"Title","room_type":"Room Type","price":"Monthly Price","tag":"Badge","image_url":"Image URL","description":"Description","beds":"Beds","meta":"Meta items (comma separated)","features":"Features (comma separated)","available":"Available Beds","active":"Active","sort_order":"Sort Order"}
    },
    "facilities":{"title":"Facilities","table":"facilities","fields":["title","icon","active","sort_order"],"labels":{"title":"Title","icon":"Icon / Emoji","active":"Active","sort_order":"Sort Order"}},
    "gallery":{"title":"Gallery","table":"gallery","fields":["title","image_url","active","sort_order"],"labels":{"title":"Title","image_url":"Image URL","active":"Active","sort_order":"Sort Order"}},
    "testimonials":{"title":"Testimonials","table":"testimonials","fields":["name","role","rating","text","avatar","active","sort_order"],"labels":{"name":"Name","role":"Role","rating":"Rating","text":"Review","avatar":"Avatar / Initials","active":"Active","sort_order":"Sort Order"}},
    "faqs":{"title":"FAQs","table":"faqs","fields":["question","answer","active","sort_order"],"labels":{"question":"Question","answer":"Answer","active":"Active","sort_order":"Sort Order"}},
}

def module_redirect(key):
    return redirect(url_for("site.module_list", key=key))

@site.get("/admin/<key>")
@admin_required
def module_list(key):
    if key not in MODULES: return "Module not found",404
    m=MODULES[key]
    rows=fetch_all(m["table"], "ORDER BY sort_order,id")
    return render_template("admin/module_list.html", key=key, module=m, rows=rows)

@site.route("/admin/<key>/add", methods=["GET","POST"])
@admin_required
def module_add(key):
    if key not in MODULES: return "Module not found",404
    m=MODULES[key]
    if request.method=="POST":
        return save_module(key, None)
    return render_template("admin/module_form.html", key=key, module=m, row=None)

@site.route("/admin/<key>/edit/<int:row_id>", methods=["GET","POST"])
@admin_required
def module_edit(key,row_id):
    if key not in MODULES: return "Module not found",404
    m=MODULES[key]
    if request.method=="POST":
        return save_module(key,row_id)
    row=fetch_one(m["table"],row_id)
    if not row: return "Not found",404
    return render_template("admin/module_form.html", key=key, module=m, row=row)

def save_module(key,row_id):
    m=MODULES[key]; fields=m["fields"]
    vals=[]
    for f in fields:
        v=request.form.get(f,"").strip()
        if f in ("active","available","beds","rating","sort_order"):
            try: v=int(v or 0)
            except: v=0
        vals.append(v)
    conn=get_connection(); cur=conn.cursor()
    if row_id is None:
        cols=",".join(fields); marks=",".join(["%s"]*len(fields))
        cur.execute(f"INSERT INTO {m['table']} ({cols}) VALUES ({marks})",vals)
        msg=f"{m['title']} item added."
    else:
        sets=",".join(f"{f}=%s" for f in fields)
        cur.execute(f"UPDATE {m['table']} SET {sets} WHERE id=%s", vals+[row_id])
        msg=f"{m['title']} item updated."
    conn.commit(); cur.close(); conn.close()
    flash(msg,"success")
    return module_redirect(key)

@site.post("/admin/<key>/delete/<int:row_id>")
@admin_required
def module_delete(key,row_id):
    if key not in MODULES: return "Module not found",404
    m=MODULES[key]
    conn=get_connection(); cur=conn.cursor()
    cur.execute(f"DELETE FROM {m['table']} WHERE id=%s",(row_id,))
    conn.commit(); cur.close(); conn.close()
    flash(f"{m['title']} item deleted.","success")
    return module_redirect(key)

@site.route("/admin/settings", methods=["GET","POST"])
@admin_required
def settings():
    row=fetch_one("settings",1)
    fields=["brand","phone","email","address","hero_eyebrow","hero_title_line1","hero_title_highlight","hero_title_line2","hero_description","hero_image","happy_residents","room_count","rating","map_url"]
    if request.method=="POST":
        vals=[request.form.get(f,"").strip() for f in fields]
        conn=get_connection(); cur=conn.cursor()
        cur.execute("UPDATE settings SET "+",".join(f"{f}=%s" for f in fields)+" WHERE id=1",vals)
        conn.commit(); cur.close(); conn.close()
        flash("Website settings updated.","success")
        return redirect(url_for("site.settings"))
    return render_template("admin/settings.html", row=row, fields=fields)

@site.get("/admin/contacts")
@admin_required
def contacts_page():
    return redirect(url_for("site.admin_dashboard"))
