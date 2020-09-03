from flask import render_template,url_for,flash,redirect,request,abort,Blueprint,current_app
from flaskBlog.posts.forms import PostForm
from flaskBlog.models import User, Post
from flask_login import login_required,current_user
import os
import json
from flaskBlog import db
posts=Blueprint('posts',__name__)


@posts.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title="New Post",form=form,legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)

@posts.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form =PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updated','success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif(request.method=="GET"):
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html',title="Update Post",form=form,legend='Post Update')

@posts.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('main.home'))

@posts.route("/debug_add_posts")
def debug_add_post():
    json_path = os.path.join(current_app.root_path, 'static', 'posts.json')
    with open(json_path) as json_file:
        data = json.load(json_file)
        for post_data in data:
            author = User.query.get(post_data['user_id'])
            post = Post(title=post_data['title'], content=post_data['content'], author=author)
            db.session.add(post)
            db.session.commit()
    flash("Posts have been added!", "success")
    return redirect(url_for('main.home'))

@posts.route("/user/<string:username>")
def user_posts(username):
    page=request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=5)
    return render_template('user_posts.html',posts=posts,user=user)

