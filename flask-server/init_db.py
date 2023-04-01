from cassandra.cluster import Cluster

def init_db(session):
    
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