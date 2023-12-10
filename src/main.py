from sql_interaction import *
from nicegui import ui

predefined_tags = {"Work": "Work", "Personal": "Personal", "Study": "Study", "Project": "Project", "Miscellaneous": "Miscellaneous"}

TEST_TITLE = ""
TEST_CONTENT = ""
TEST_TAG = ""

@ui.refreshable
def cards():
    notes = get_notes_with_tags()
    with ui.row().classes("w-full h-full"):
            for note in notes:
                note_id, title, content, created_at, updated_at, tags = note
                with ui.card():
                    with ui.row():
                        ui.label(note_id).style("font-size: 12px; color: gray")
                        ui.label(tags).style("font-size: 12px; color: gray")
                        ui.label(title).style("font-size: 18px")
                    ui.markdown(content)
                    ui.label(f"Created: {created_at} | Updated: {updated_at}").style("font-size: 8px")

def submit_note(title_element, tag_element, content_element, diag):
    add_note(title_element, content_element)

    add_new_tag(tag_element)

    link_note_to_tag(title_element, tag_element)
    cards.refresh()
    diag.close()

@ui.page("/")
def mainp():
    ui.dark_mode(True)

    with ui.dialog().classes("w-full") as dialog, ui.card().classes("w-full"):
        with ui.column():
            title_ = ui.input("Title", placeholder="My Favorite Title!").props('rounded outlined dense')
            tag_ = ui.select(options=predefined_tags)
            content_ = ui.editor(placeholder="Note Content").props('rounded outlined dense')
            ui.button("Submit", on_click=lambda e: submit_note(str(title_.value), str(tag_.value), str(content_.value), dialog))
            ui.button("Cancel", on_click=dialog.close)

    notes = []

    try:
        notes = get_notes_with_tags()
    except sqlite3.OperationalError:
        print("Creating Tables")
        create_DB()
        initialize_tags()

    if len(notes) == 0:
        with ui.card().classes("absolute-center items-center"):
            ui.label("You have no notes!")
            ui.button("+", on_click=dialog.open)
    else:
        ui.button("+", on_click=dialog.open)
        cards()

ui.run()