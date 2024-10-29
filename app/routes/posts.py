from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from typing import Union, Optional
from models import db
from models.posts import Post  # import the Post model
from forms.posts import PostForm

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/view', methods=['GET'])
def view_posts() -> Union[str, Response]:
    """Render the posts page with all posts from the database."""
    posts = Post.query.all()
    form = PostForm()  # Create an instance of the form
    return render_template('posts.html', posts=posts, form=form)

@posts_bp.route('/create', methods=['GET','POST'])
def create_post() -> Response:
    """Display and handle the creation of a new post."""
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title = form.title.data,
            content = form.content.data
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('posts.view_posts'))
    else:
        flash('Title and content are required to create a post.', 'danger')
    return render_template('create_post.html', form=form)

@posts_bp.route('/update/<int:post_id>', methods=['GET','POST'])
def update_post(post_id: int) -> Response:
    """Handle updating an existing post."""
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)  # Populate the form with the existing post data
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('posts.view_posts'))
    else:
        flash('Title and content are required to update a post.', 'danger')
    return render_template('update_post.html', form=form)
    
@posts_bp.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id: int) -> Response:
    """Handle deleting a post."""
    post = Post.query.get_or_404(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
    else:
        flash('Post not found.', 'danger')
    return redirect(url_for('posts.view_posts'))
    
