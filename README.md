# Trading game: getting started

## Run the game
1. Open your Codespace.
2. Choose **Terminal → New Terminal** and enter:
   ```bash
   python server.py
   ```
3. Open **Ports**, then choose **Open in Browser** beside port **8000**. Keep the port **Private**.

The starter displays your inputs but does not yet play the game.

## Start coding
Open `game.py`. The supplied `handle_action(action, fields, database)` function receives the button pressed, text entered in the boxes, and a connection to your database. It returns the text shown in the game window.

Replace the demonstration with your own code. Choose your own functions, files and database structure. Use the browser’s input boxes rather than Python’s `input()`.

After changing Python code, stop the running server with **Ctrl+C**, run `python server.py` again, and refresh the game page.

## Work with your database
`game.sqlite3` stores your tables and data. Open it with **SQLite3 Editor**, not the text editor.

1. Open `game.sqlite3` in Explorer. If needed, right-click it and choose **Open With… → SQLite3 Editor**.
2. Click **Query Editor**. Keep the database-link comment on the first line.
3. Write your SQL below that comment. Click **Execute** above a statement, or place the cursor in it and press **Shift+Enter**.
4. Save the query editor as `queries.sql` in your project so you keep your SQL work.

Saving the SQL file does not execute it. Your Python game uses the same database through its `database` connection.

Python database changes are saved automatically when `handle_action` returns text normally. If it raises an exception or returns something other than text, that action is rolled back. Check inputs before changing data: returning an error message is still a normal return and saves any changes already made. Use the supplied `database` connection and leave transaction control to the server (no manual commit/rollback, transaction commands or `executescript` inside the callback). This is separate from GitHub **Commit** and **Sync Changes** below.

## Save your work and finish
1. Open **Source Control**:&nbsp; &nbsp; <img src="web/images/Source Control Icon.png" alt="Source Control icon" align="middle">
2. Enter a short description of what you changed and choose **Commit**:&nbsp; &nbsp; <img src="web/images/Message and Commit Button.png" alt="Message field and commit button" align="middle">
3. Choose **Sync Changes** to push your work to GitHub. Wait for it to finish.
4. Go to [your Codespaces](https://github.com/codespaces), open the **…** menu beside this Codespace and choose **Stop codespace**.

Stopping the Codespace also stops the game server. Closing the browser tab alone does not immediately stop the Codespace.
