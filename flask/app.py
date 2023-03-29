from cassandra.cluster import Cluster
from flask import Flask, request, render_template, redirect, url_for
import uuid

app = Flask(__name__, template_folder='templates')

# Connect to Cassandra cluster
cluster = Cluster(['cassandra1', 'cassandra2', 'cassandra3'])
session = cluster.connect()

# Create keyspaces and tables if they don't exist
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS videos 
    WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};
""")
session.execute("""
    CREATE TABLE IF NOT EXISTS videos.video_names (
        video_id uuid PRIMARY KEY,
        video_name text
    );
""")
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS comments 
    WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};
""")
session.execute("""
    CREATE TABLE IF NOT EXISTS comments.video_comments (
        video_id uuid,
        comment_id uuid,
        username text,
        comment text,
        PRIMARY KEY ((video_id), comment_id)
    ) WITH CLUSTERING ORDER BY (comment_id ASC);
""")

# Serve video list page
@app.route('/')
def video_list():
    result = session.execute("""
        SELECT video_id, video_name FROM videos.video_names
    """)
    videos = [{'id': row.video_id, 'name': row.video_name} for row in result]
    return render_template('video_list.html', videos=videos)


@app.route('/add_video', methods=['POST'])
def add_video():
    video_name = request.form.get('video_name')
    video_id = uuid.uuid4()  # Generate a new UUID for the video
    
    # Insert video
    session.execute("""
        INSERT INTO videos.video_names (video_id, video_name)
        VALUES (%s, %s)
    """, (video_id, video_name))
    
    # Redirect to video list page
    return redirect(url_for('video_list'))

# Serve video comments page
@app.route('/video/<uuid:video_id>')
def video_comments(video_id):
    result = session.execute("""
        SELECT video_name FROM videos.video_names WHERE video_id = %s
    """, (video_id,))
    video_name = result[0].video_name if result else None
    
    result = session.execute("""
            SELECT comment_id, username, comment FROM comments.video_comments
            WHERE video_id = %s
        """, (video_id,)
    )
    comments = [{'id': row.comment_id, 'username': row.username, 'comment': row.comment} for row in result]
    return render_template('video_comments.html', video_id=video_id, video_name=video_name, comments=comments)

# Handle comment submissions
@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    video_id = request.form.get('video_id')
    comment_username = request.form.get('comment_username')
    comment_text = request.form.get('comment_text')
    comment_id = uuid.uuid4()  # Generate a new UUID for the comment
    
    # Insert comment
    session.execute("""
        INSERT INTO comments.video_comments (video_id, comment_id, username, comment)
        VALUES (%s, %s, %s, %s)
    """, (uuid.UUID(video_id), comment_id, comment_username, comment_text))
    
    # Redirect to video comments page
    return redirect(url_for('video_comments', video_id=video_id))

# Delete comment
@app.route('/delete_comment/<uuid:comment_id>')
def delete_comment(comment_id):
    result = session.execute("""
        SELECT video_id FROM comments.video_comments WHERE comment_id = %s
    """, (comment_id,))
    video_id = result.one().video_id if result else None
    
    session.execute("""
        DELETE FROM comments.video_comments WHERE comment_id = %s ALLOW FILTERING
    """, (comment_id,))
    
    # Redirect to video comments page
    return redirect(url_for('video_comments', video_id=video_id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)