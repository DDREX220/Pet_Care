from flask import session, redirect, url_for, flash

def login_required(f):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def admin_required(f):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("auth.login"))
        if session.get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("auth.dashboard"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper