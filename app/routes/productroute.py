from flask import Blueprint
from app.controllers.productcontroller import ProductController


class ProductRoutes:
    def __init__(self):
        self.bp = Blueprint("product", __name__)
        self.controller = ProductController()

    def register(self):
        self.bp.add_url_rule("/getproduct", view_func=self.controller.get_product, methods=["GET", "POST"])
        self.bp.add_url_rule("/addproduct", view_func=self.controller.add_product, methods=["GET", "POST"])
        self.bp.add_url_rule("/deleteproduct", view_func=self.controller.delete_product, methods=["GET", "POST"])
        return self.bp