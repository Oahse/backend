# backend

---

# **Backend Setup Guide**

## **1. Set Up a Virtual Environment**

A virtual environment ensures that your project's dependencies are isolated from the global Python environment.

### **Step 1: Create a Virtual Environment**

```bash
python3 -m venv venv
```

This command will create a virtual environment named `venv` in your project directory.

### **Step 2: Activate the Virtual Environment**

- **On macOS/Linux**:
    ```bash
    source venv/bin/activate
    ```

- **On Windows**:
    ```bash
    venv\Scripts\activate
    ```

After activating the virtual environment, your terminal prompt should now start with `(venv)` indicating that the virtual environment is active.

## **2. Install Dependencies**

Once the virtual environment is active, install the required dependencies listed in the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

This will install all the necessary Python packages needed to run the project, including Django and any other required packages.

### **Note**: Ensure you have a `requirements.txt` file in the root directory of your project that includes all necessary dependencies. To create or update this file with your project's current dependencies, use the following command:

```bash
pip freeze > requirements.txt
```

## **3. Apply Database Migrations**

Before running the server, apply the necessary database migrations to set up your database schema.

```bash
python manage.py migrate
```

This command will apply all migrations to the database, ensuring your database structure is up to date with the latest models.

## **4. Run the Development Server**

Once everything is set up, you can start the Django development server with the following command:

```bash
python manage.py runserver
```

The server will start, and you should see an output similar to this:

```plaintext
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Open your web browser and navigate to `http://127.0.0.1:8000/` to view your application.

---

### **Additional Notes**:

- **Deactivate Virtual Environment**: Once you're done, you can deactivate the virtual environment by running:
  
  ```bash
  deactivate
  ```

- **Updating Requirements**: Whenever you install a new package, remember to update your `requirements.txt` file using:
  
  ```bash
  pip freeze > requirements.txt
  ```

---
