from flask import render_template, request
from app.models.tip import Tip
from app.auth import login_required

class TipController:

    def view_tips(self):
        tips = Tip.get_all()
        return render_template("tips/view_tips.html", tips=tips)

    def view_tip_detail(self, tip_id):
        tip = Tip.get_by_id(tip_id)
        if not tip:
            return render_template("errors/404.html"), 404
        return render_template("tips/tip_detail.html", tip=tip)

    def search_tips(self):
        keyword = request.args.get("keyword", "")
        tips = []
        if keyword:
            tips = Tip.search(keyword)
        return render_template("tips/search_tips.html", 
                               tips=tips, keyword=keyword)