from flask import Blueprint
from app.controllers.productcontroller import ProductController
class ProductRoutes:
    def __init__(self):
        self.bp = Blueprint("product", __name__)
        self.controller = ProductController()

    def register(self):
        self.bp.route("/getproduct", methods=["GET","POST"]) (
            self.controller.login
        )
        self.bp.route("/addproduct", methods=["GET","POST"])(
            self.controller.register
        )
        self.bp.route("/deleteproduct", methods=["GET","POST"])(
            self.controller.register
        )
        return self.bp