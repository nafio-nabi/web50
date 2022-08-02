# Capstone Project: Schleplist

## Distinctiveness and Complexity
<br>

The name of my project is [schleplist](https://schleplist.herokuapp.com/). It is a web application to share tedious, unpleasant tasks (schleps) of users. The application allows users to sign up, sign in, and sign out. After signing up, a user can share a textual description of their schleps. It also allows users to bookmarks other user's schleps. Additionally, users can customize their profile by uploading their profile picture. Lastly, their is a public list of all schleps that any visitor can see without signing up.

I have developed and deployed the app to production using: HTML CSS, JavaScript, and Bootstrap on the front-end. In the backend-end I have used Python, Django, PostgreSQL. For production deployment I have used Heroku for compute and database, and Cloudinary for static file hosting.

The reason why my project satisfies the distinctiveness and complexity requirements is: (i) it is not a social network, nor an ecommerce site. It is a public forum type web app, (ii) It utilizes Django: views, templates, models (thee custom models), and forms. Additionally it uses JavaScript on the front-end by implementing AJAX for submitting form data without full page reset, (iv) Lastly, it is mobile-responsive.

The files I have commited code to are:

- views.py: 
     - signup, signin, signout functions for authentication.
     - new_post function for making new posts.
     - edit_post function for edition an existing post.
     - all_post function for listing all posts.
     - post function for listing an individual post.
     - bookmarks function for creating, and removing bookmarks.
     - profile function to show an users profile.
     - settings function to edit an user's profile.

- models.py: 
     - User class for creating a user.
     - UserManager class to modify custom user model to make email mandatory instead of username.
     - NewPost class for creating a new post.
     - Bookmarks class for creating bookmarks.

- templates: 
     - all_posts.html
     - post.html
     - new_post.html
     - profile.html
     - settings.html
     - signin.html
     - signup.html
     - bookmarks.html
     - index.html
     - navbar.html
     - footer.html

- forms.py: 
     - SignUpForm class to sign up users.
     - SignInForm class to sign in users.
     - NewPostForm class to make a new post.
     - ImageUploadForm to upload user image.
     - BookmarkForm to make a new bookmark.

- urls.py: 
     - index path
     - signup path
     - signout path
     - signin path
     - new_post path
     - edit_post path
     - all_posts path
     - post path
     - bookmarks path
     - profile path
     - settings path

- static/: 
     - app.js
     - main.css
     - bootstrap.bundle.min.js
     - bootstrap.min.css

- Procfile for Heroku deployment.

- runtime.txt for Heroku deployment.

- requirements.txt

To run the application go through the following steps:

- Clone repository:
     ```bash
     git clone https://github.com/nafio-nabi/web50.git
     cd web50/projects/2020/x/capstone/
     ```

- Create and activate virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

- Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

- Run migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

- Run development server:
     ```bash
     python manage.py runserver