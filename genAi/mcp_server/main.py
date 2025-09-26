from mcp.server.fastmcp import FastMCP
import sqlite3
from datetime import datetime

# Initialize our MCP server with the name "todos"
mcp = FastMCP("todos")

# --- Database Setup ---
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
async def list_todos():
    """Lists all todos from the database."""
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
    todos = cursor.fetchall()
    conn.close()
    return [{"id": t[0], "title": t[1], "description": t[2], "status": t[3]} for t in todos]

@mcp.tool()
async def update_todo_status(todo_id: int, status: str):
    """Updates the status of a todo."""
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE todos SET status = ?, updated_at = ? WHERE id = ?",
        (status, datetime.now().isoformat(), todo_id)
    )
    conn.commit()
    conn.close()
    return {"id": todo_id, "status": status}

@mcp.tool()
async def delete_todo(todo_id: int):
    """Deletes a todo from the database."""
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return {"deleted": todo_id}

# --- Run the Server ---
if __name__ == "__main__":
    mcp.run(transport="stdio")
