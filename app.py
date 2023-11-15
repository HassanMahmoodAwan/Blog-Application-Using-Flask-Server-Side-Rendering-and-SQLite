# For rendering HTML, use render_template with Ninja in HTML FILE
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# To Check the request Type from user
from flask import request, redirect


# Initializing an App
app = Flask(__name__)

# You need to Configure your DataBase in APP
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# Initializing the Database
db = SQLAlchemy(app)

# Variables
all_posts = [
    {'Title': 'Python',
     'Author': 'Hassan Mahmood',
     'Detail': 'Functional Programming'},

    {'Title': 'Object Oriented Programming',
     'Detail': 'Class-Object Concepts'}

]


# Creating a Table in the Database
class BlogPost(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    Author= db.Column(db.String(100), nullable=False, default='N/A')
    Detail = db.Column(db.String(100), nullable=False)
    DateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # To repeat Adding every Blog Post, using the Method
    def __repr__(self):
        return 'blogPost'+ str(self.Id)






# Creating an Home Route
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# Blog Post Route
@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        # db.create_all()   # Run before putting app values
        title = request.form['title']
        Author = request.form['author']
        Detail = request.form['detail']
        new_blog = BlogPost(Title = title, Author = Author, Detail = Detail)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.DateTime).all()
        return render_template('blog.html', allpost=all_posts)


# Route for Deleting the Blog
@app.route('/blog/delete/<int:Id>')
def blog_delete(Id):
    post = BlogPost.query.get_or_404(Id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/blog')
   

# Route for Updating the Content
@app.route('/blog/edit/<int:Id>', methods=['GET', 'POST'])
def edit_blog(Id):
    blog = BlogPost.query.get_or_404(Id)
    if request.method == 'POST':
        blog.Title =  request.form['title']
        blog.Author =  request.form['author']
        blog.Detail =  request.form['detail']
        db.session.commit()
        return redirect('/blog')
    else:
        return render_template('edit.html', post = blog)


# Runing an App on default LocalHost Address
if __name__ == '__main__':
    app.run(debug=True)