# Django Blog Authentication System

## Overview
This authentication system provides user registration, login, logout, and profile management for the Django blog project. It uses Django's built-in authentication framework and custom forms/views for registration and profile editing.

## Features
- User registration with email
- User login/logout
- Profile view and update (username, email)
- CSRF protection on all forms
- Secure password handling

## How It Works
- **Registration:** Users register via `/register/` using a form that extends Django's `UserCreationForm` to include email. On success, the user is logged in and redirected to their profile.
- **Login:** Users log in at `/login/` using Django's built-in authentication view.
- **Logout:** Users log out at `/logout/`.
- **Profile:** Authenticated users can view and update their username and email at `/profile/`.

## Setup Instructions
1. Ensure `'blog'` is in `INSTALLED_APPS` in `settings.py`.
2. Include `path('', include('blog.urls'))` in your main `urls.py`.
3. Place the provided templates in `blog/templates/blog/` and ensure your `TEMPLATES` setting includes `'APP_DIRS': True`.
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`

## User Guide
- Register: Go to `/register/` and fill out the form.
- Login: Go to `/login/` and enter your credentials.
- Logout: Click the logout link on the profile page or go to `/logout/`.
- Profile: Go to `/profile/` to view or update your info.

## Security Notes
- All forms use CSRF tokens.
- Passwords are securely hashed by Django.
- Only authenticated users can access the profile page.

## Testing
- Try registering a new user and logging in/out.
- Update your profile and verify changes.
- Attempt to access `/profile/` when not logged in (should redirect to login).
