import sqlite3

def create_DB():
    conn = sqlite3.connect('my_notes.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Execute the SQL statements to create the tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS Notes (
                        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        content TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Tags (
                        tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tag_name TEXT UNIQUE)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS NoteTags (
                        note_id INTEGER,
                        tag_id INTEGER,
                        PRIMARY KEY (note_id, tag_id),
                        FOREIGN KEY (note_id) REFERENCES Notes(note_id) ON DELETE CASCADE,
                        FOREIGN KEY (tag_id) REFERENCES Tags(tag_id) ON DELETE CASCADE)''')

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

def get_notes_by_tag(tag_name):
    conn = sqlite3.connect('my_notes.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT Notes.note_id, Notes.title, Notes.content, Notes.created_at, Notes.updated_at
                      FROM Notes
                      JOIN NoteTags ON Notes.note_id = NoteTags.note_id
                      JOIN Tags ON NoteTags.tag_id = Tags.tag_id
                      WHERE Tags.tag_name = ?''', (tag_name,))

    notes = cursor.fetchall()
    conn.close()
    return notes

def get_notes_with_tags():
    conn = sqlite3.connect('my_notes.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT Notes.note_id, Notes.title, Notes.content, Notes.created_at, Notes.updated_at, GROUP_CONCAT(Tags.tag_name) as tags
                      FROM Notes
                      LEFT JOIN NoteTags ON Notes.note_id = NoteTags.note_id
                      LEFT JOIN Tags ON NoteTags.tag_id = Tags.tag_id
                      GROUP BY Notes.note_id, Notes.title, Notes.content, Notes.created_at, Notes.updated_at''')

    notes_with_tags = cursor.fetchall()
    conn.close()
    return notes_with_tags

def add_note(title, content):
    conn = sqlite3.connect('my_notes.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

def add_tag(tag_name):
    conn = sqlite3.connect('my_notes.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Tags (tag_name) VALUES (?)", (tag_name,))
    conn.commit()
    conn.close()

# Predefined tags
predefined_tags = ["Work", "Personal", "Study", "Project", "Miscellaneous"]

# Function to initialize predefined tags in the database
def initialize_tags():
    conn = sqlite3.connect('my_notes.db')
    cursor = conn.cursor()
    for tag in predefined_tags:
        cursor.execute("INSERT OR IGNORE INTO Tags (tag_name) VALUES (?)", (tag,))
    conn.commit()
    conn.close()

# Function to add a new tag
def add_new_tag(new_tag):
    if new_tag not in predefined_tags:
        predefined_tags.append(new_tag)  # Add to the in-memory list
        conn = sqlite3.connect('my_notes.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO Tags (tag_name) VALUES (?)", (new_tag,))
        conn.commit()
        conn.close()

def link_note_to_tag(note_title, tag_name):
    conn = sqlite3.connect('my_notes.db')
    cursor = conn.cursor()

    # Get note_id
    cursor.execute("SELECT note_id FROM Notes WHERE title = ?", (note_title,))
    note_id = cursor.fetchone()[0]

    # Get tag_id
    cursor.execute("SELECT tag_id FROM Tags WHERE tag_name = ?", (tag_name,))
    tag_id = cursor.fetchone()[0]

    # Link note to tag
    cursor.execute("INSERT INTO NoteTags (note_id, tag_id) VALUES (?, ?)", (note_id, tag_id))
    conn.commit()
    conn.close()