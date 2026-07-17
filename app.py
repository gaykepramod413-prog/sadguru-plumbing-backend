import io
import os
from datetime import date

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

import mysql.connector
from mysql.connector import Error

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black

# ======================================================================
# DATABASE CONFIG (Render Compatible)
# ======================================================================

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "1234"),
    "database": os.environ.get("DB_NAME", "sadguru_plumbing")
}


def get_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            category VARCHAR(100) NOT NULL,
            sizes VARCHAR(255) NOT NULL,
            unit VARCHAR(30) NOT NULL
        )
    """)

    conn.commit()

    cursor.close()
    conn.close()


# ======================================================================
# PDF BRANDING
# ======================================================================

BUSINESS_NAME = "SADGURU PLUMBING"
CONTRACTOR_NAME = "Contractor: Kanifnath Ashok Gayke"

THEME_COLOR = HexColor("#0F6E56")
THEME_COLOR_LIGHT = HexColor("#E1F5EE")
ROW_ALT_COLOR = HexColor("#F5FAF8")

PAGE_WIDTH, PAGE_HEIGHT = A4

LEFT_MARGIN = 40
RIGHT_MARGIN = PAGE_WIDTH - 40

HEADER_HEIGHT = 90

COL_SN = LEFT_MARGIN
COL_NAME = LEFT_MARGIN + 30
COL_SIZE = LEFT_MARGIN + 260
COL_UNIT = LEFT_MARGIN + 350
COL_QTY = LEFT_MARGIN + 420


def draw_plumbing_icon(c, x, y):
    c.saveState()

    c.setStrokeColor(white)
    c.setLineWidth(3)

    c.line(x, y, x + 26, y)

    c.circle(x + 4, y, 5)
    c.circle(x + 22, y, 5)

    c.line(x + 10, y - 10, x + 22, y - 22)

    c.circle(x + 9, y - 9, 4)
    c.circle(x + 23, y - 23, 4)

    c.restoreState()


def draw_header(c):

    top_y = PAGE_HEIGHT

    c.setFillColor(THEME_COLOR)

    c.rect(
        0,
        top_y - HEADER_HEIGHT,
        PAGE_WIDTH,
        HEADER_HEIGHT,
        stroke=0,
        fill=1
    )

    draw_plumbing_icon(c, LEFT_MARGIN, top_y - 40)

    c.setFillColor(white)

    c.setFont("Helvetica-Bold", 20)
    c.drawString(
        LEFT_MARGIN + 45,
        top_y - 34,
        BUSINESS_NAME
    )

    c.setFont("Helvetica", 11)
    c.drawString(
        LEFT_MARGIN + 45,
        top_y - 52,
        CONTRACTOR_NAME
    )

    c.setFont("Helvetica", 9)
    c.drawString(
        LEFT_MARGIN + 45,
        top_y - 68,
        "Plumbing Material Requirement List"
    )

    c.drawRightString(
        RIGHT_MARGIN,
        top_y - 34,
        f"Date : {date.today().strftime('%d/%m/%Y')}"
    )


def draw_job_info(c, y, customer_name, site_name):

    c.setFillColor(black)

    c.setFont("Helvetica-Bold", 11)

    if customer_name:
        c.drawString(
            LEFT_MARGIN,
            y,
            f"Customer : {customer_name}"
        )
        y -= 16

    if site_name:
        c.drawString(
            LEFT_MARGIN,
            y,
            f"Site : {site_name}"
        )
        y -= 16

    return y - 6


def draw_table_header(c, y):

    c.setFillColor(THEME_COLOR_LIGHT)

    c.rect(
        LEFT_MARGIN,
        y - 22,
        RIGHT_MARGIN - LEFT_MARGIN,
        22,
        stroke=0,
        fill=1
    )

    c.setFillColor(THEME_COLOR)

    c.setFont("Helvetica-Bold", 10)

    c.drawString(COL_SN + 4, y - 15, "#")
    c.drawString(COL_NAME, y - 15, "Material")
    c.drawString(COL_SIZE, y - 15, "Size")
    c.drawString(COL_UNIT, y - 15, "Unit")
    c.drawRightString(COL_QTY + 60, y - 15, "Qty")

    return y - 22


# ======================================================================
# FLASK APP
# ======================================================================

app = Flask(__name__)

CORS(app)


@app.route("/")
def home():
    return "Sadguru Plumbing Backend is Running Successfully!"
# ======================================================================
# MATERIAL API ROUTES
# ======================================================================

@app.route("/api/materials", methods=["GET"])
def get_materials():

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM materials
            ORDER BY category, name
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        result = []

        for row in rows:

            result.append({
                "id": row["id"],
                "name": row["name"],
                "category": row["category"],
                "unit": row["unit"],
                "sizes": [
                    s.strip()
                    for s in row["sizes"].split(",")
                ]
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ----------------------------------------------------------
# GET ALL CATEGORIES
# ----------------------------------------------------------

@app.route("/api/materials/categories", methods=["GET"])
def get_categories():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT category
            FROM materials
            ORDER BY category
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        categories = [row[0] for row in rows]

        return jsonify(categories)

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ----------------------------------------------------------
# ADD NEW MATERIAL
# ----------------------------------------------------------

@app.route("/api/materials", methods=["POST"])
def add_material():

    try:

        data = request.get_json(force=True)

        name = data.get("name")
        category = data.get("category")
        sizes = data.get("sizes")
        unit = data.get("unit")

        if not name:
            return jsonify({"message": "Material name required"}), 400

        if not category:
            return jsonify({"message": "Category required"}), 400

        if not sizes:
            return jsonify({"message": "Sizes required"}), 400

        if not unit:
            return jsonify({"message": "Unit required"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO materials
            (
                name,
                category,
                sizes,
                unit
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
        """,
        (
            name,
            category,
            sizes,
            unit
        ))

        conn.commit()

        material_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "id": material_id,
            "message": "Material Added Successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ----------------------------------------------------------
# DELETE MATERIAL
# ----------------------------------------------------------

@app.route("/api/materials/<int:id>", methods=["DELETE"])
def delete_material(id):

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM materials WHERE id=%s",
            (id,)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Material Deleted"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    # ======================================================================
# PDF GENERATION
# ======================================================================

@app.route("/api/pdf/generate", methods=["POST"])
def generate_pdf():

    try:

        data = request.get_json(force=True)

        customer_name = data.get("customerName", "")
        site_name = data.get("siteName", "")
        items = data.get("items", [])

        if len(items) == 0:
            return jsonify({
                "success": False,
                "message": "No material selected."
            }), 400

        buffer = io.BytesIO()

        pdf = canvas.Canvas(buffer, pagesize=A4)

        draw_header(pdf)

        y = PAGE_HEIGHT - HEADER_HEIGHT - 20

        y = draw_job_info(
            pdf,
            y,
            customer_name,
            site_name
        )

        y = draw_table_header(pdf, y)

        pdf.setFont("Helvetica", 10)

        row_height = 22

        for index, item in enumerate(items):

            if y < 60:

                pdf.showPage()

                draw_header(pdf)

                y = PAGE_HEIGHT - HEADER_HEIGHT - 20

                y = draw_table_header(pdf, y)

                pdf.setFont("Helvetica", 10)

            if index % 2 == 1:

                pdf.setFillColor(ROW_ALT_COLOR)

                pdf.rect(
                    LEFT_MARGIN,
                    y - row_height,
                    RIGHT_MARGIN - LEFT_MARGIN,
                    row_height,
                    stroke=0,
                    fill=1
                )

            pdf.setFillColor(black)

            pdf.drawString(
                COL_SN + 4,
                y - 15,
                str(index + 1)
            )

            pdf.drawString(
                COL_NAME,
                y - 15,
                str(item.get("name", ""))
            )

            pdf.drawString(
                COL_SIZE,
                y - 15,
                str(item.get("size", ""))
            )

            pdf.drawString(
                COL_UNIT,
                y - 15,
                str(item.get("unit", ""))
            )

            pdf.drawRightString(
                COL_QTY + 60,
                y - 15,
                str(item.get("quantity", ""))
            )

            y -= row_height

        pdf.setStrokeColor(THEME_COLOR)

        pdf.line(
            LEFT_MARGIN,
            y - 4,
            RIGHT_MARGIN,
            y - 4
        )

        pdf.setFillColor(HexColor("#555555"))

        pdf.setFont("Helvetica", 9)

        pdf.drawString(
            LEFT_MARGIN,
            y - 20,
            BUSINESS_NAME
        )

        pdf.drawString(
            LEFT_MARGIN,
            y - 34,
            CONTRACTOR_NAME
        )

        pdf.setFillColor(HexColor("#888888"))

        pdf.setFont("Helvetica", 8)

        pdf.drawString(
            LEFT_MARGIN,
            y - 50,
            "This is a computer generated material requirement list."
        )

        pdf.save()

        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="material-list.pdf"
        )

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ======================================================================
# START SERVER (Render Ready)
# ======================================================================

if __name__ == "__main__":

    try:

        init_db()

        print("=" * 60)
        print(" Sadguru Plumbing Backend Started ")
        print("=" * 60)
        print("Database :", DB_CONFIG["database"])
        print("Host     :", DB_CONFIG["host"])
        print("=" * 60)

    except Error as e:

        print("Database Connection Failed")
        print(e)

    PORT = int(os.environ.get("PORT", 3000))

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=True
    )
    