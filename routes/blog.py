import datetime
import ast
import redis
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    jsonify,
    json)

from models.blog import Blog
from models.blog_comment import BlogComment
from routes import blog_owner_required, blog_comment_owner_required, current_user, login_required, new_csrf_token, \
    csrf_required

main = Blueprint('blog', __name__)
cache = redis.StrictRedis()


@main.route('/new')
def new():
    token = new_csrf_token()
    u = current_user()
    v = cache.get("site_translate_list").decode('utf-8')
    tranlates = json.loads(v)
    return render_template('/blog/blog_new.html', user=u, token=token, tranlates=tranlates)


# 删除功能：
# 有一个删除按钮
# 按下之后，首先要判断是不是这个博客的所有者
# 如果是，那么后端数据库删掉这个数据
# 结束后前端也要删掉这个数据
# 如果不是，那么前台范围警告
@main.route('/delete')
@blog_owner_required
def delete():
    print("blog delete start")
    blog_id = int(request.args['id'])
    print("delete blog_id", blog_id)
    Blog.delete(blog_id)
    BlogComment.delete_all(blog_id)
    d = dict(
        message="成功删除 blog"
    )
    return jsonify(d)


@main.route('/api/delete', methods=['POST'])
@login_required
def api_delete():
    form_str = request.data.decode()
    form = ast.literal_eval(form_str)
    blog_id = int(form['id'])
    print("delete blog_id", blog_id)
    Blog.delete(id=blog_id)
    BlogComment.delete_all(blog_id)
    d = dict(
        message="成功删除 blog"
    )
    return jsonify(d)


@main.route('/comment/delete')
@blog_comment_owner_required
def delete_comment():
    comment_id = int(request.args['id'])
    comment = BlogComment.one(id=comment_id)
    print("comment_id", comment)
    BlogComment.delete(comment_id)
    d = dict(
        message="成功删除 comment",
    )
    return jsonify(d)


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    print("blog request.form", request.form)
    form = request.form.to_dict()
    Blog.new(form, u)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect(url_for('blog.index'))


@main.route('/detail')
@login_required
def detail():
    jsonify("detail start")
    blog_id = request.args['id']
    blog = Blog.one(id=blog_id)
    comments = BlogComment.all(blog_id=blog_id)
    u = current_user()
    token = new_csrf_token()
    # now_time = datetime.datetime.now()
    # created_time = datetime.datetime.fromtimestamp(int(blog.created_time))
    # delta = now_time - created_time
    # hours = round(delta.total_seconds() // 3600 - delta.days*24)
    # minutes = round((delta.total_seconds() % 3600) // 60)
    # seconds = round(delta.total_seconds() - minutes * 60)
    # if delta.days > 0:
    #     diff = "{}日{}時間".format(delta.days, hours)
    # elif hours > 0 and delta.days <= 0:
    #     # diff = delta.days + "時間" + delta.minutes + "分"
    #     diff = "{}時間{}分".format(hours, minutes)
    # elif minutes > 0 and hours <= 0:
    #     # diff = delta.minutes + "分" + delta.seconds + "秒"
    #     diff = "{}分{}秒".format(minutes, seconds)
    # elif delta.minutes <= 0:
    #     # diff = delta.seconds + "秒"
    #     diff = "{}秒".format(delta.seconds)

    v = cache.get("site_translate_list").decode('utf-8')
    created_time = datetime.datetime.fromtimestamp(blog.created_time)
    tranlates = json.loads(v)
    return render_template('blog/blog_detail.html', blog=blog, comments=comments, user=u, token=token, time=created_time, tranlates=tranlates)


@main.route('/index',methods=['GET'], defaults={"page": 1})
@main.route('/index/<int:page>', methods=['GET'])
@login_required
def index(page):
    u = current_user()
    # blogs = Blog.all(user_id=u.id)
    # blogs = Blog.all()
    page = page
    per_page = 10
    blogs = Blog.query.paginate(page, per_page, error_out=False)
    # for pp in blogs.iter_pages():
    #     print(pp)
    v = cache.get("site_translate_list").decode('utf-8')
    tranlates = json.loads(v)
    # 替换模板文件中的标记字符串
    return render_template('blog/blog_index.html', blogs=blogs, user=u, tranlates=tranlates)


@main.route('/update', methods=['POST'])
@login_required
# @blog_owner_required
def update():
    jsonify("log update start")
    form = request.form
    blog_id = int(form['id'])
    print("blog_id", blog_id)
    content = form['content']
    print("content", content)
    Blog.update(blog_id, content=content)
    return redirect(url_for('blog.detail', id=blog_id))


@main.route('/api/update_title', methods=['POST'])
@login_required
def update_title():
    form_str = request.data.decode()
    form = ast.literal_eval(form_str)
    blog_id = int(form['id'])
    title = form['title']
    Blog.update(blog_id, tlitle=title)
    d = dict(
        message="成功"
    )
    return jsonify(d)


@main.route('/comment/add', methods=['POST'])
@login_required
# @csrf_required
def comment_add():
    # 实现评论的 comment_add 路由
    u = current_user()
    form = request.form.to_dict()
    blog = Blog.one(id=int(form['blog_id']))
    c = BlogComment()
    c.content = form.get('content', '')
    c.user_id = u.id
    c.blog_id = blog.id
    BlogComment.new(c.__dict__, u)
    return redirect(url_for('blog.detail', id=blog.id))
