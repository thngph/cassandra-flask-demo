from cassandra.cluster import Cluster
from flask import Flask
from init_db import init_db
from routes import *

app = Flask(__name__, template_folder='templates')

# Connect to Cassandra cluster
session = Cluster(['cassandra1', 'cassandra2', 'cassandra3']).connect()
init_db(session)
session.shutdown()



app.add_url_rule('/', 'video_list', video_list) # Serve video list page
app.add_url_rule('/add_video', 'add_video', add_video, methods=['POST']) # Insert video
app.add_url_rule('/update_video/<uuid:video_id>', 'update_video', update_video, methods=['POST'])
app.add_url_rule('/delete_video/<uuid:video_id>', 'delete_video', delete_video) # Delete comment
app.add_url_rule('/video/<uuid:video_id>', 'video_comments', video_comments) # Serve video list page
app.add_url_rule('/submit_comment', 'submit_comment', submit_comment, methods=['POST']) # Insert comment
app.add_url_rule('/delete_comment/<uuid:video_id>/<uuid:comment_id>', 'delete_comment', delete_comment) # Delete comment

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)