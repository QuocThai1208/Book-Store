from flask import session

from app import app, db
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView  # ModelView dung de tao view tren model
from app.models import Category, Book, Author
from flask import request
import utils


class CategoryView(ModelView):
    column_list = ['name', 'books']

class AuthorView(ModelView):
    column_list = ['name', 'books']


class BookView(ModelView):
    pass



# Ghi đè trang chủ admin để lấy dữ liệu
class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=utils.category_stats())


class StatsView(BaseView):

    @expose('/')
    def index(self):
        return self.render('template_admin/index.html')


admin = Admin(app=app,
              name="Library Administration",
              template_mode='bootstrap4',
              index_view = MyAdminIndex()
              )

admin.add_view(CategoryView(Category, db.session))
admin.add_view(AuthorView(Author, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(StatsView(name='Stats'))
