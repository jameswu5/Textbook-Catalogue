## Textbook Catalogue by James Wu

Here is the [video demonstration](https://drive.google.com/file/d/13BvYECq_vHFlQqq9PB-u4zx_JxvEUxiL/view?usp=sharing) of this project, and the documentation is provided [here](https://docs.google.com/document/d/1lM54LGNAJIdutLrYdjUYV7UoZPIYz8kQVtrM763r_eQ/edit?usp=sharing).

This project uses Flask (Python), HTML and SQLite 3. To operate:

- Run database.py first to create the database and populate the tables with mock data.
- Run main.py and click on the Flask link to use.
- The mock data comes with 3 accounts to log in with:
  - Username admin password admin to access an account with admin status
  - Username teacher password teacher to access an account with teacher status
  - Username student password student to access an account with student status.

### Note:
When creating a new account through the admin, the new account's password is defaulted to "password". The new user can then log in with "password" and will be prompted to change their password.
If the Flask server restarts in the middle of using the page then you'll likely be redirected to an error page if you click on a link. In this case, you only need to log back in.
