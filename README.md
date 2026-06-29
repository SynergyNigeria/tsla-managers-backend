# TSA Managers Django Backend

Run migrations:

```powershell
cd backend
python manage.py migrate
```

Start the local server:

```powershell
python manage.py runserver 127.0.0.1:8765
```

Then open the API:

```text
http://127.0.0.1:8765
```

Submitted applications are stored in SQLite at `backend/db.sqlite3`.
Uploaded files are stored in `backend/media/applications/<application-id>/`.

## Separate frontend and backend hosting

The frontend can be hosted as static files from the `frontend` folder. Before
uploading it, set the backend URL in `frontend/config.js`:

```js
window.TSA_API_BASE = "https://yourusername.pythonanywhere.com";
```

The Django backend can be hosted separately on PythonAnywhere. Set the WSGI
module to `tsa_manager.wsgi.application` and set the working directory to the
`backend` folder.

Recommended PythonAnywhere environment variables:

```text
DEBUG=0
SECRET_KEY=replace-this-with-a-long-secret-value
ALLOWED_HOSTS=yourusername.pythonanywhere.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

For local development with separate hosting, run Django on
`http://127.0.0.1:8765` and keep `frontend/config.js` pointed there.

The backend does not serve the frontend in production. The root URL returns a
small API health response, while the actual website is served by the separate
frontend host.

## REST endpoints

- `POST /api/applications`
  - Accepts `multipart/form-data` from the manager application form.
  - Requires ID proof.
  - CV is optional and must be PDF when included.

- `GET /api/applications/{applicationId}?email={email}`
  - Returns the public status fields for an application.

## Updating application status

Create an admin user:

```powershell
python manage.py createsuperuser
```

Then open `/admin/`, choose an application, and update the `status` field to:

- `Pending review`
- `Accepted`
- `Rejected`

Applicants will see the updated value on `status.html` after checking with
their application ID and email.
