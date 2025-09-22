from mcp.server.fastmcp import FastMCP
import sqlite3
from datetime import datetime

# Initialize our MCP server with the name "todos"
mcp = FastMCP("todos")

# --- Database Setup ---
# This function creates our database and table if they don't exist.
def init_db():
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT,
        updated_at TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Run the database setup when the server starts
init_db()

# --- MCP Tools ---
# These are the functions our AI will be able to call.

@mcp.tool()
async def add_todo(title: str, description: str = ""):
    """Adds a new todo to the database."""
    now = datetime.now().isoformat()
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO todos (title, description, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (title, description, now, now)
    )
    todo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id": todo_id, "title": title, "status": "pending"}


@mcp.tool()
async def get_all_todo():
    """Return all the todos from the database."""
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, status, created_at, updated_at FROM todos")
    rows = cursor.fetchall()
    conn.close()

    todos = [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "created_at": row[4],
            "updated_at": row[5],
        }
        for row in rows
    ]
    return todos
    
# --- Run the Server ---
if __name__ == "__main__":
    mcp.run(transport="stdio")
