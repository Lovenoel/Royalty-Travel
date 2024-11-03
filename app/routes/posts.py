from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from typing import Union, Optional
from models import db
from models.posts import Post  # import the Post model
from forms.posts import PostForm
from flask_login import login_required, current_user

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/view/<int:post_id>', methods=['GET'])
@login_required
def view_posts(post_id) -> Union[str, Response]:
    """Render the posts page with all posts from the database."""
    # posts = Post.query.all()
    form = PostForm()  # Create an instance of the form

    posts = Post.query.get_or_404(post_id)
    # Allow access if post is public or current user is the author
    if posts.is_public or posts.author_id == current_user.id:
        return render_template('view_post.html', post=posts)
    else:
        flash("You are not authorized to view this post.")
        return redirect(url_for('home'))
    return render_template('posts.html', posts=posts, form=form)

@posts_bp.route('/create', methods=['GET','POST'])
@login_required
def create_post() -> Response:
    """Display and handle the creation of a new post."""
    post = Post.query.all()
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title = form.title.data,
            content = form.content.data,
            is_public=form.is_public.data,
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('posts.view_posts'))
    else:
        flash('Title and content are required to create a post.', 'danger')
    return render_template('create_post.html', form=form, post_id=post.id)

@posts_bp.route('/update/<int:post_id>', methods=['GET','POST'])
@login_required
def update_post(post_id: int) -> Response:
    """Handle updating an existing post."""
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)  # Populate the form with the existing post data
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_public = form.is_public.data
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('posts.view_posts'))
    else:
        flash('Title and content are required to update a post.', 'danger')
    return render_template('update_post.html', form=form)
    
@posts_bp.route('/delete/<int:post_id>', methods=['POST'])
@login_required
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
    
@posts_bp.route('/list_posts')
@login_required
def list_posts():
    """Display a list of posts accessible to the current user."""
    # Show only public posts or posts created by the current user
    posts = Post.query.filter(
        (Post.is_public == True) | (Post.author_id == current_user.id)
    ).all()
    return render_template('list_posts.html', posts=posts)