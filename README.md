# EduValut
Here's your guide with **only the HTML and CSS filenames renamed** to match the `EduVault` project structure you've shown earlier:

---

# Setting Up a Python-Flask Application on a Linux Instance

This guide provides step-by-step instructions to set up a Flask application on a Linux instance with HTTP and custom TCP protocols.

---

## Steps to Set Up the Linux Instance

1. **Create a Linux instance**.
2. **Enable HTTP Server**:

   * Keep the server `http` on.
   * Ensure the port range is set to **80**.
3. **Create Custom TCP Protocol**:

   * Add a custom TCP protocol with the server port range **5000**.

---

## After Launching the Linux Instance

### Connect to the Instance

1. Open the console and connect to the Linux instance.

### Commands to Set Up the Environment and Application

Below are the commands to set up the Flask application:

1. Switch to the root user:

   ```bash
   sudo su
   ```
2. Install Apache HTTP server:

   ```bash
   yum install httpd
   ```
3. Start the HTTP service:

   ```bash
   service httpd start
   ```
4. Install Python 3:

   ```bash
   sudo yum install python3 -y
   ```
5. Install GCC and Python development tools:

   ```bash
   sudo yum install gcc python3-devel -y
   ```
6. Install `virtualenv`:

   ```bash
   sudo yum install python3-virtualenv -y
   ```
7. Create a project directory:

   ```bash
   mkdir EduVault
   ```
8. Navigate into the project directory:

   ```bash
   cd EduVault
   ```
9. Create a Python virtual environment:

   ```bash
   python3 -m venv venv
   ```
10. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```
11. Install Flask and Gunicorn:

    ```bash
    pip install Flask gunicorn
    ```
12. Create the main application file:

    ```bash
    vim app.py
    ```
13. Create directories for templates, static files, and uploads:

    ```bash
    mkdir templates
    mkdir static
    mkdir uploads
    ```

### Create HTML Templates:

```bash
cd templates
vim login.html
vim register.html
vim welcome.html
vim uploads.html
vim superuser_dashboard.html
vim courses.html
cd ..
```

### Create CSS Stylesheets:

```bash
cd static
vim login.css
vim welcome.css
vim uploads.css
vim superuser_dashboard.css
vim courses.css
cd ..
```

---

## Running the Project

Start the server using Gunicorn:

```bash
gunicorn -w 1 -b 0.0.0.0:5000 app:app
```

* `-w 1`: One worker.
* `-b 0.0.0.0:5000`: Bind to all network interfaces on port 5000.
* `app:app`: Refers to `app.py`'s Flask instance named `app`.

---

## Notes

* Replace `EduVault` with any other name if needed.
* Use `vim`, `nano`, or any preferred text editor to edit files.
* Ensure all dependencies are correctly installed before running the app.

---

Let me know if you'd like a downloadable `.zip` of this starter project or a GitHub-compatible version!
