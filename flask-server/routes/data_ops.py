from flask import request, render_template, redirect, url_for
import uuid
from helpers.session import *

# Connect to Cassandra cluster
session = init_session()



# -------------------------------------------------------------------------

def video_list():
    check_session(session)
    result = session.execute("""
        SELECT video_id, video_name FROM videos.video_names
    """)
    videos = [{'id': row.video_id, 'name': row.video_name} for row in result]

    return render_template('video_list.html', videos=videos)



def add_video():
    check_session(session)
    video_name = request.form.get('video_name')
    video_id = uuid.uuid4() 
    session.execute("""
        INSERT INTO videos.video_names (video_id, video_name)
        VALUES (%s, %s)
    """, (video_id, video_name)) # Insert video

    return redirect(url_for('video_list')) # Redirect to video list page



def delete_video(video_id):
    check_session(session)
    session.execute("""
        DELETE FROM videos.video_names WHERE video_id = %s""", (video_id,))
    session.execute("""
        DELETE FROM comments.video_comments WHERE video_id = %s""", (video_id,))

    return redirect(url_for('video_list')) # Redirect to video comments page



def update_video(video_id):
    check_session(session)
    new_video_name = request.form.get('new_video_name')
    session.execute("""
        UPDATE videos.video_names SET video_name = %s WHERE video_id = %s
    """, (new_video_name, video_id)) # Update video name

    return redirect(url_for('video_list')) # Redirect to video list page



# ------------------------------------------------------------------------------------

def video_comments(video_id):
    check_session(session)
    result = session.execute("""
        SELECT video_name FROM videos.video_names WHERE video_id = %s
    """, (video_id,))
    video_name = result[0].video_name if result else None
    result = session.execute("""
            SELECT comment_id, username, comment FROM comments.video_comments
            WHERE video_id = %s
        """, (video_id,) )
    comments = [{'id': row.comment_id, 'video_id': video_id,
                 'username': row.username, 'comment': row.comment} for row in result]
    
    return render_template('video_comments.html', video_id=video_id, video_name=video_name, comments=comments)


def submit_comment():
    check_session(session)
    video_id = request.form.get('video_id')
    comment_username = request.form.get('comment_username')
    comment_text = request.form.get('comment_text')
    comment_id = uuid.uuid4()  
    session.execute("""
        INSERT INTO comments.video_comments (video_id, comment_id, username, comment)
        VALUES (%s, %s, %s, %s)
    """, (uuid.UUID(video_id), comment_id, comment_username, comment_text)) # Insert comment

    return redirect(url_for('video_comments', video_id=video_id)) # Redirect to video comments page



def delete_comment(video_id, comment_id):
    check_session(session)
    session.execute("""
        DELETE FROM comments.video_comments WHERE video_id = %s AND comment_id = %s""", (video_id, comment_id))

    return redirect(url_for('video_comments', video_id=video_id)) # Redirect to video comments page