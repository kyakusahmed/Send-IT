from app.views import app2
from flask import jsonify, render_template


@app2.route('/user/login', methods=['GET'])
def login():
    """Render user login page"""
    return render_template('index.html')

@app2.route('/user/register', methods=['GET'])
def register_user():
    """Render user register page."""
    return render_template('SignUp.html')

# @app.route('/admin/orders', methods=['GET'])
# def admin_orders_page():
#     """Render admin orders page."""
#     return render_template('admin/orders.html')

# @app.route('/admin/menus', methods=['GET'])
# def admin_get_all_menus_page():
#     """Render admin menus page."""
#     return render_template('admin/menus/index.html')

# @app.route('/admin/menus/create', methods=['GET'])
# def admin_add_menu_page():
#     """Render admin add menu page."""
#     return render_template('admin/menus/create.html')

# @app.route('/admin/menus/<int:menu_id>/edit', methods=['GET'])
# def admin_edit_specific_menu_page(menu_id):
#     """Render admin edit a menu page."""
#     return render_template('admin/menus/edit.html', menu_id=menu_id)

# @app.route('/admin/menus/<int:menu_id>', methods=['GET'])
# def admin_get_specific_menu_page(menu_id):
#     """Render admin get a menu page."""
#     return render_template('admin/menus/show.html', menu_id=menu_id)

# @app.route('/admin/orders/history', methods=['GET'])
# def admin_get_menu_history_page():
#     """Render admin get menu history page."""
#     return render_template('admin/history.html')

# @app.route('/user/orders/history', methods=['GET'])
# def user_get_order_history_page():
#     """Render user order history page."""
#     return render_template('history.html')