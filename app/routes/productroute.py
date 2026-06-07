from flask import Blueprint
from ..controllers.productcontroller import ProductController
class ProductRoutes:
    def __init__(self):
        self.bp = Blueprint("product", __name__)
        self.controller = ProductController()

    def register(self):
        self.bp.route("/getproduct", methods=["GET","POST"]) (
            self.controller.get_product
        )
        self.bp.route("/addproduct", methods=["GET","POST"])(
            self.controller.add_product
        )
        self.bp.route("/deleteproduct", methods=["GET","POST"])(
            self.controller.delete_product
        )
        return self.bp