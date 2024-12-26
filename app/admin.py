from app import app, db
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView  # ModelView dung de tao view tren model
from app.models import Category, Book, Author, Image
import utils


class CategoryView(ModelView):
    column_sortable_list = []
    column_list = ['name']

class ImageView(ModelView):
    column_sortable_list = []
    column_list = ['name', 'books']

class AuthorView(ModelView):
    column_sortable_list = []
    column_list = ['name', 'books']


class BookView(ModelView):
    column_sortable_list = []


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

admin.add_view(CategoryView(Category, db.session))
admin.add_view(AuthorView(Author, db.session))
admin.add_view(ImageView(Image, db.session))
admin.add_view(BookView(Book, db.session))


