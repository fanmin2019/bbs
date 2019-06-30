import time

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    jsonify,
)

from models.blog import Blog
from models.blog_comment import BlogComment
from routes import blog_owner_required, blog_comment_owner_required, current_user, login_required, new_csrf_token, \
    csrf_required

main = Blueprint('blog', __name__)


@main.route('/new')
def new():
    token = new_csrf_token()
    u = current_user()
    return render_template('/blog/blog_new.html', user=u, token=token)


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
    now_time = int(time.time())
    diff = now_time - int(blog.created_time)
    diff = round(diff / 60 / 60)

    return render_template('blog/blog_detail.html', blog=blog, comments=comments, user=u, token=token, time=diff)


@main.route('/index')
@login_required
def index():
    """
    weibo 首页的路由函数
    """
    u = current_user()
    # blogs = Blog.all(user_id=u.id)
    blogs = Blog.all()
    # 替换模板文件中的标记字符串
    return render_template('blog/blog_index.html', blogs=blogs, user=u)


@main.route('/update', methods=['POST'])
@login_required
# @blog_owner_required
def update():
    print("wahaha")
    jsonify("log update start")
    form = request.form
    blog_id = int(form['id'])
    print("blog_id", blog_id)
    content = form['content']
    print("content", content)
    Blog.update(blog_id, content=content)
    return redirect(url_for('blog.detail', id=blog_id))


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
