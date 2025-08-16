# Blog Post CRUD Features

## Overview
This feature enables users to create, read, update, and delete blog posts in the Django blog project. Authenticated users can manage their own posts, while all users can view posts.

## Features
- **ListView:** `/posts/` shows all blog posts.
- **DetailView:** `/posts/<pk>/` shows a single post.
- **CreateView:** `/posts/new/` allows logged-in users to create posts.
- **UpdateView:** `/posts/<pk>/edit/` allows authors to edit their posts.
- **DeleteView:** `/posts/<pk>/delete/` allows authors to delete their posts.

## Permissions
- Only authenticated users can create posts.
- Only the author can edit or delete their posts.
- All users can view the list and detail pages.

## How to Use
- Go to `/posts/` to see all posts.
- Click a post title to view details.
- If logged in and you are the author, you can edit or delete your posts.
- Use the "Create New Post" link to add a new post (must be logged in).

## Notes
- All forms are protected with CSRF tokens.
- Author is set automatically to the logged-in user.
- Navigation links are provided for user convenience.

## Testing
- Test creating, editing, and deleting posts as an authenticated user.
- Ensure unauthorized users cannot edit or delete posts they do not own.
- Check that all links and navigation work as expected.
