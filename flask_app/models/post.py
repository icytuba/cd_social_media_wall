from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Post:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.content = db_data['content']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.creator = None

    @staticmethod
    def validate_post(post):
        is_valid=True
        if len(post['new_post'])<1:
            flash("Post cannot be blank")
            is_valid=False
        return is_valid
    
    @classmethod
    def create_post(cls, data):
        query = "INSERT INTO posts (user_id, content) VALUES (%(user_id)s, %(content)s);"
        return connectToMySQL('wall_schema').query_db(query, data)

    @classmethod
    def get_all_posts_with_creator(cls):
        query = "SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC;"
        results = connectToMySQL('wall_schema').query_db(query)
        all_posts = []
        for row in results:
            one_post = cls(row)
            author_info ={
                'id':row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password':row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            author = user.User(author_info)
            one_post.creator = author
            all_posts.append(one_post)
        return all_posts
    
    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts WHERE id=%(id)s;"
        return connectToMySQL('wall_schema').query_db(query, data)
