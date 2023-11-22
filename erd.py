from eralchemy2 import render_er

from app.blog.infra.database import DATABASE_URL

# Draw from database
render_er(DATABASE_URL, 'erd_from_sqlite.png')
