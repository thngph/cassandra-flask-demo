from cassandra.cluster import Cluster
from flask import request, render_template, redirect, url_for
import uuid

# Connect to Cassandra cluster
cluster = Cluster(['cassandra1', 'cassandra2', 'cassandra3'])
session = cluster.connect()



def video_list():
    result = session.execute("""
        SELECT video_id, video_name FROM videos.video_names
    """)
    videos = [{'id': row.video_id, 'name': row.video_name} for row in result]
    return render_template('video_list.html', videos=videos)


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

def delete_video(video_id):
    session.execute("""
        DELETE FROM videos.video_names WHERE video_id = %s""", (video_id,))
    
    session.execute("""
        DELETE FROM comments.video_comments WHERE video_id = %s""", (video_id,))
    
    # Redirect to video comments page
    return redirect(url_for('video_list'))

def update_video(video_id):
    new_video_name = request.form.get('new_video_name')
    
    # Update video name
    session.execute("""
        UPDATE videos.video_names SET video_name = %s WHERE video_id = %s
    """, (new_video_name, video_id))
    
    # Redirect to video list page
    return redirect(url_for('video_list'))


#------------------------------------------------------------------------------------

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
    comments = [{'id': row.comment_id, 'video_id': video_id, 'username': row.username, 'comment': row.comment} for row in result]
    return render_template('video_comments.html', video_id=video_id, video_name=video_name, comments=comments)


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


def delete_comment(video_id, comment_id):
    
    session.execute("""
        DELETE FROM comments.video_comments WHERE video_id = %s AND comment_id = %s""", (video_id, comment_id))
    
    # Redirect to video comments page
    return redirect(url_for('video_comments', video_id=video_id))