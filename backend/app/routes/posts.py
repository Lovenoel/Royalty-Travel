from . import db
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from ..forms.posts import PostForm
from ..models.Post import Post

post_bp = Blueprint('post', __name__, url_prefix='/post')

@post_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title = form.title.data,
            content = form.content.data,
            author = current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('index'))
    return render_template('create_posts.html', title='New Post', form=form)