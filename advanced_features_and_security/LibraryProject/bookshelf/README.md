# Permissions

### Models(bookshefl/models.py)

Custom Permissions Book Model

- `can_view`: Allows viewing of a book instance.
- `can_create`: Allows creation of a new book instance.
- `can_edit`: Allows editing of an existing book instance.
- `can_delete`: Allows deletion of a book instance.


### Views
Views check if user has permission to carry out action, If they do not they are served an error


### Groups
- **Viewers:** Have `can_view` permission.
- **Editors:** Have `can_create` and `can_edit` permissions.
- **Admins:** Have all four permissions (`can_view`, `can_create`, `can_edit`, `can_delete`).
