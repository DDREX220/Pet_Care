from flask import flash, render_template, request
from pymysql import MySQLError

from app.database import connection_scope, ensure_schema


class ProductController:
    def get_product(self):
        if request.method == "POST":
            product_id = request.form.get("product_id", "").strip()

            if not product_id:
                flash("Product ID is required.")
                return render_template("getproduct.html", product_id=product_id), 400

            try:
                ensure_schema()
                with connection_scope() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
                        product = cursor.fetchone()

                if product is None:
                    flash(f"No product found for ID {product_id}.")
                    return render_template("getproduct.html", product_id=product_id), 404

                return render_template("getproduct.html", product=product, product_id=product_id)
            except MySQLError as error:
                flash(f"Database error: {error}")
                return render_template("getproduct.html", product_id=product_id), 500

        return render_template("getproduct.html")
    
    def add_product(self):
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            category = request.form.get("category", "").strip()
            price = request.form.get("price", "").strip()
            quantity = request.form.get("quantity", "").strip()

            if not name or not category or not price or not quantity:
                flash("All product fields are required.")
                return render_template(
                    "addproduct.html",
                    name=name,
                    category=category,
                    price=price,
                    quantity=quantity,
                ), 400

            try:
                ensure_schema()
                with connection_scope() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO products (name, category, price, quantity) VALUES (%s, %s, %s, %s)",
                            (name, category, price, quantity),
                        )
                        product_id = cursor.lastrowid
                    connection.commit()

                flash(f"Product {name} was saved with ID {product_id}.")
                return render_template(
                    "addproduct.html",
                    name=name,
                    category=category,
                    price=price,
                    quantity=quantity,
                    product_id=product_id,
                )
            except MySQLError as error:
                flash(f"Database error: {error}")
                return render_template(
                    "addproduct.html",
                    name=name,
                    category=category,
                    price=price,
                    quantity=quantity,
                ), 500

        return render_template("addproduct.html")
    
    def delete_product(self):
        if request.method == "POST":
            product_id = request.form.get("product_id", "").strip()

            if not product_id:
                flash("Product ID is required.")
                return render_template("deleteproduct.html", product_id=product_id), 400

            try:
                ensure_schema()
                with connection_scope() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
                        deleted_count = cursor.rowcount
                    connection.commit()

                if deleted_count == 0:
                    flash(f"No product found for ID {product_id}.")
                    return render_template("deleteproduct.html", product_id=product_id), 404

                flash(f"Product {product_id} deleted.")
                return render_template("deleteproduct.html", product_id=product_id, deleted=True)
            except MySQLError as error:
                flash(f"Database error: {error}")
                return render_template("deleteproduct.html", product_id=product_id), 500

        return render_template("deleteproduct.html")