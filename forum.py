# forum.py

from bottle import Bottle, request, redirect, template
import sqlite3

# Create the Bottle application
app = Bottle()

# Define the database connection and create the posts table
conn = sqlite3.connect('forum.db')
conn.execute('''CREATE TABLE IF NOT EXISTS posts
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              content TEXT NOT NULL);''')

# Define the routes
@app.route('/')
def index():
    # Retrieve all posts from the database and format them for display
    posts = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    formatted_posts = format_posts(posts)

    # Render the HTML template for the index page
    return template('index.html', posts=formatted_posts)

@app.route('/new')
def new_post():
    # Render the HTML template for the new post page
    return template('new_post.html')

@app.post('/add_post')
def add_post():
    # Get the title and content of the new post from the request form
    title = request.forms.get('title')
    content = request.forms.get('content')

    # Get the uploaded file and check its size
    upload = request.files.get('upload')
    if upload and upload.file:
        size = len(upload.file.read())
        if size > 15 * 1024 * 1024:  # 15MB limit
            return 'File size limit exceeded (15MB)'
        else:
            filename = upload.filename
            # Save the uploaded file
            upload.save('./uploads/' + filename)

    # Insert the new post into the database and commit the transaction
    conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
    conn.commit()

    # Redirect the user back to the index page
    redirect('/')


# Define a function to format posts for display
def format_posts(posts):
    result = ''
    for post in posts:
        result += '''
            <div class="post">
                <h2><a href="/post/{id}" target="_blank">{title}</a></h2>
                <p>{content}</p>
            </div>
        '''.format(id=post[0], title=post[1], content=post[2])
    return result

@app.route('/post/<id:int>')
def view_post(id):
    # Retrieve the post from the database
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()

    # Retrieve all comments for the post from the database
    comments = conn.execute("SELECT * FROM comments WHERE post_id = ? ORDER BY id", (id,)).fetchall()

    # Render the HTML template for the post page
    return template('post.html', post=post, comments=comments)


@app.post('/add_comment')
def add_comment():
    # Get the post ID and comment content from the request form
    post_id = request.forms.get('post_id')
    content = request.forms.get('content')

    # Check if the content field is empty or null
    if not content:
        return 'Comment content cannot be empty'

    # Insert the new comment into the database and commit the transaction
    conn.execute("INSERT INTO comments (post_id, content) VALUES (?, ?)", (post_id, content))
    conn.commit()

    # Redirect the user back to the post page
    redirect('/post/{}'.format(post_id))



# Start the Bottle application
if __name__ == '__main__':
    app.run(debug=True)
