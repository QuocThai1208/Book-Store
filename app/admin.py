from flask import session

from app import app, db
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView  # ModelView dung de tao view tren model
from app.models import Category, Book, Author
import utils




class BookView(ModelView):
    can_view_details = True
    can_export = True
    # column_list = ['id', 'Name', 'Author_id', 'Year_model', 'UnitPrice', 'Code', 'image', 'UnitsInStock', 'Category_id']

# Ghi đè trang chủ admin để lấy dữ liệu
class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=utils.category_stats())


admin = Admin(app=app,
              name="Library Administration",
              template_mode='bootstrap4',
              index_view = MyAdminIndex()
              )

admin.add_view(ModelView(Category, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(ModelView(Author, db.session))
