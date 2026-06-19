from flask import render_template
class ProductController:
    def login(self):
        return render_template("addproduct.html")
    
    def register(self):
        return render_template("getproduct.html")
    
    def register(self):
        return render_template("deleteproduct.html")