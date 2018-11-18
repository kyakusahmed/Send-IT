from app.views.admin import app2
from app.views.user import app2
from app.models.migrations import Migration


if __name__ == "__main__":
    db_conn = Migration()
    db_conn.create_tables() 
    db_conn.drop_tables()
    db_conn.create_tables()  
    app2.run(debug=True, port=8080)