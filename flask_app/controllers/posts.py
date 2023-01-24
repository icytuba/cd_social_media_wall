from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import post
from flask import flash

@app.route('/process/post', methods=['POST'])
def process_post():
    if not post.Post.validate_post(request.form):
        return redirect(f"/wall/{session['user_id']}")
    data={
        'user_id': request.form['user_id'],
        'content': request.form['new_post']
    }
    post.Post.create_post(data)
    return redirect(f"/wall/{session['user_id']}")




@app.route('/delete/post/<int:post_id>')
def delete_post(post_id):
    data={
        'id': post_id
    }
    post.Post.delete_post(data)
    return redirect(f"/wall/{session['user_id']}")
# need to work on this and the html to make sure the post id is communicated correctly to be deleted 