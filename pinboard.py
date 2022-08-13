import atexit
from datetime import datetime, timezone
import json
import os
import sqlite3
import sys
from typing import Dict, List, Tuple
from urllib import request

apiURL = "https://api.pinboard.in/v1"
apiToken = os.getenv("pinboard_api_token")
apiParams = {"auth_token": apiToken, "format": "json"}

rfc3339 = "%Y-%m-%dT%H:%M:%SZ"

def main():
    db = sqlite3.connect("pinboard.db")
    atexit.register(db.close)

    init_tables(db)
    sync(db)

    terms = []
    if len(sys.argv) > 1:
        terms = sys.argv[1].split(" ")
    matching_posts = query_posts(db, terms)
    print(format_items(matching_posts))

def format_items(rows: List[Tuple[str, str, str]]) -> str:
    n = len(rows)
    items = [format_item(idx, n, row) for (idx, row) in enumerate(rows)]
    return json.dumps({"items": items})

def format_item(idx: int, n: int, row: Tuple[str, str, str]) -> Dict[str, str]:
    pos = 100 - round(10 * idx / n) * 10
    (description, href, tags) = row
    return {
        "title": description,
        "subtitle": tags,
        "arg": href,
        "icon": {
            "path": "blue-{}.png".format(pos),
        },
    }

def query_posts(db: sqlite3.Connection, query_values: List[str]):
    if len(query_values) == 0:
        rows = db.execute("SELECT description, href, tags FROM posts ORDER BY ts DESC").fetchall()
        return rows
    wheres = []
    for qv in query_values:
        if qv == "":
            continue
        qor = []
        qor.append("description LIKE '%{}%'".format(qv))
        qor.append("href LIKE '%{}%'".format(qv))
        qor.append("tags LIKE '%{}%'".format(qv))
        wheres.append("({})".format(" OR ".join(qor)))
    where = " AND ".join(wheres)
    query = "SELECT description, href, tags FROM posts WHERE {} ORDER BY ts DESC".format(where)
    rows = db.execute(query).fetchall()
    return rows

def init_tables(db: sqlite3.Connection) -> None:
    db.execute("""
    CREATE TABLE IF NOT EXISTS meta (
        key TEXT,
        value TEXT,
        UNIQUE (key) ON CONFLICT REPLACE
    )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        hash TEXT,
        href TEXT,
        description TEXT,
        extended TEXT,
        tags TEXT,
        ts TIMESTAMP
    )
    """)

def sync(db: sqlite3.Cursor, local: bool = False) -> None:
    if needs_posts_sync(db):
        posts = get_posts(local)
        increment_get_posts_count(db)
        save_posts(db, posts)
        db.commit()

def needs_posts_sync(db: sqlite3.Connection) -> bool:
    last_sync = db.execute("SELECT value FROM meta WHERE key = 'posts_sync'").fetchone()
    if not last_sync:
        return True

    last_sync = datetime.strptime(last_sync[0], rfc3339).replace(tzinfo=timezone.utc)
    now = datetime.now(tz=timezone.utc)
    # API rate limit is once per 5 minutes
    return (now - last_sync).seconds > 300

def get_posts(local: bool = False) -> List[Dict[str, str]]:
    if local:
        # load from local file for development
        with open("pinboard.json") as f:
            return json.load(f)

    params = apiParams.copy()
    params = ["{}={}".format(k, params[k]) for k in params]
    u = "{}/posts/all?{}".format(apiURL, "&".join(params))
    headers = {
        "X-App-ID": "quells_alfred-2.0-d8171",
    }
    req = request.Request(method="GET", url=u, headers=headers)
    resp = request.urlopen(req, timeout=30.0)
    if resp.status != 200:
        raise Exception("failed to get posts")

    return json.loads(resp.read())

def increment_get_posts_count(db: sqlite3.Connection) -> None:
    key = "get_posts_count"
    cur = db.execute("UPDATE meta SET value = value + 1 WHERE key = ?", (key,))
    if cur.rowcount == 0:
        db.execute("INSERT INTO meta (key, value) VALUES (?, 1)", (key,))

def save_posts(db: sqlite3.Connection, posts: List[Dict[str, str]]) -> None:
    db.execute("DELETE FROM posts WHERE 1=1")

    for post in posts:
        values = (
            post.get("hash"),
            post.get("href"),
            post.get("description"),
            post.get("extended"),
            post.get("tags"),
            post.get("time"),
        )
        db.execute("""
            INSERT INTO posts
                (hash, href, description, extended, tags, ts)
            VALUES
                (?, ?, ?, ?, ?, ?)
            """,
            values,
        )

    now = datetime.strftime(datetime.utcnow(), rfc3339)
    db.execute("INSERT INTO meta (key, value) VALUES ('posts_sync', ?)", (now,))

if __name__ == "__main__":
    main()
