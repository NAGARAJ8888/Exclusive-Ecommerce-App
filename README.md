# Exclusive E-Commerce Application 🛒[<a href="https://nagarajbotekar.pythonanywhere.com/" target="_blank">LINK</a>]

An advanced Django-based e-commerce platform with Stripe integration for secure payments.

## 🚀 Features
- User authentication (Register/Login)
- Products search & filter
- Shopping wishlist, cart & checkout
- Stripe payment gateway
- Order history & email confirmations


## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+ installed
- Node.js and npm installed
- Git (for cloning)

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NAGARAJ8888/Exclusive-Ecommerce-App.git
   cd Exclusive-Ecommerce-App
   ```

2. **Navigate to the project directory:**
   ```bash
   cd ecom
   ```

3. **Set up Python Virtual Environment:**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install Node.js Dependencies:**
   ```bash
   # Install root dependencies
   npm install
   
   # Install theme dependencies for Tailwind CSS
   cd theme/static_src
   npm install
   cd ../..
   ```

6. **Set up Database (Required for Production):**
   
   **For Local Development (SQLite - Default):**
   - No setup needed! The app uses SQLite by default for local development.
   
   **For Production (MySQL on PythonAnywhere):**
   
   a. **Create MySQL Database on PythonAnywhere:**
      - Log into your PythonAnywhere account
      - Go to the "Databases" tab
      - Click "Create a new database"
      - Note down your database credentials:
        - Database name (usually `yourusername$default`)
        - Username (usually your PythonAnywhere username)
        - Password (set during database creation)
        - Host (usually `yourusername.mysql.pythonanywhere-services.com`)
   
   b. **Set Environment Variables:**
      - In PythonAnywhere, go to "Web" tab → "Web app" → "Environment variables"
      - Add these variables:
        ```
        USE_MYSQL=true
        DB_NAME=your_database_name
        DB_USER=your_username
        DB_PASSWORD=your_password
        DB_HOST=your_username.mysql.pythonanywhere-services.com
        DB_PORT=3306
        ```
      - Or create a `.env` file in the `ecom` directory with the same variables
   
   c. **Install MySQL Client:**
      ```bash
      pip install mysqlclient
      ```
      > Note: On PythonAnywhere, mysqlclient is usually pre-installed. If installation fails on Windows, you can use PyMySQL as an alternative (see troubleshooting section).

7. **Set up Environment Variables (Optional for Stripe):**
   Create a `.env` file in the `ecom` directory (or set environment variables):
   ```bash
   STRIPE_PUBLIC_KEY=your_stripe_public_key
   STRIPE_SECRET_KEY=your_stripe_secret_key
   ```
   > Note: The app will work without Stripe keys, but payment functionality will be disabled.

8. **Run Database Migrations:**
   ```bash
   python manage.py migrate
   ```
   > **Important:** After switching to MySQL, you'll need to run migrations again to create all tables in the new database.

9. **Create a Superuser (Optional - for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

10. **Collect Static Files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

11. **Build Tailwind CSS (for development):**
    ```bash
    cd theme/static_src
    npm run dev
    ```
    Keep this terminal running in the background to watch for CSS changes.

12. **Start the Django Development Server:**
    Open a new terminal (keep the Tailwind one running) and run:
    ```bash
    cd ecom
    python manage.py runserver
    ```

13. **Access the Application:**
    - Open your browser and go to: `http://127.0.0.1:8000/`
    - Admin panel: `http://127.0.0.1:8000/admin/` (if you created a superuser)

### Quick Start (If dependencies are already installed)

If you've already completed the setup once:

```bash
cd ecom
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # macOS/Linux

# In one terminal - Start Tailwind CSS watcher
cd theme/static_src
npm run dev

# In another terminal - Start Django server
cd ecom
python manage.py runserver
```

## 🔧 Troubleshooting

### MySQL Database Issues

**Problem: `mysqlclient` installation fails on Windows**
- **Solution:** Use PyMySQL as an alternative. Add this to your `settings.py` before the DATABASES configuration:
  ```python
  import pymysql
  pymysql.install_as_MySQLdb()
  ```
  Then install PyMySQL: `pip install PyMySQL` and add it to `requirements.txt`

**Problem: Database connection errors on PythonAnywhere**
- **Solution:** 
  - Verify all environment variables are set correctly in the Web app settings
  - Check that your database name includes your username prefix (e.g., `yourusername$default`)
  - Ensure your database password is correct
  - Verify the host is `yourusername.mysql.pythonanywhere-services.com`

**Problem: "Table doesn't exist" after switching to MySQL**
- **Solution:** Run migrations again:
  ```bash
  python manage.py migrate
  ```

**Problem: Migrating data from SQLite to MySQL**
- **Solution:** Use Django's `dumpdata` and `loaddata`:
  ```bash
  # Export from SQLite (with USE_MYSQL=false)
  python manage.py dumpdata > data.json
  
  # Switch to MySQL (set USE_MYSQL=true)
  # Run migrations first
  python manage.py migrate
  
  # Import to MySQL
  python manage.py loaddata data.json
  ```

### Other Issues

**Problem: Static files not loading**
- **Solution:** Run `python manage.py collectstatic --noinput` after any static file changes

**Problem: Tailwind CSS not updating**
- **Solution:** Make sure the Tailwind watcher is running: `cd theme/static_src && npm run dev`


- The project Screenshots

<img width="1920" height="1080" alt="Screenshot-1" src="https://github.com/user-attachments/assets/5313fd7a-37ac-48eb-a19a-76c9ceaf5b4e" />
<img width="1920" height="1080" alt="Screenshot-2" src="https://github.com/user-attachments/assets/a833f3a2-08a8-4830-9b02-e9d191921ab2" />
<img width="1920" height="1080" alt="Screenshot-3" src="https://github.com/user-attachments/assets/8d5a707e-3fca-40ee-b7e3-30d59ea6e6a5" />
<img width="1920" height="1080" alt="Screenshot-4" src="https://github.com/user-attachments/assets/6ec8f01f-f3eb-4873-9475-a73516087848" />
<img width="1920" height="1080" alt="Screenshot-5" src="https://github.com/user-attachments/assets/2b47c715-706b-42ee-803a-d3bfc2ce14eb" />
<img width="1920" height="1080" alt="Screenshot-6" src="https://github.com/user-attachments/assets/f2d5ef45-979f-4b9b-bc3a-fe08b2ea1d9f" />
<img width="1920" height="1080" alt="Screenshot-7" src="https://github.com/user-attachments/assets/512b4625-a576-4b19-96a6-0be4c6bdf203" />
<img width="1920" height="1080" alt="Screenshot-8" src="https://github.com/user-attachments/assets/6fddb6b1-7e40-4fbc-b4e2-5f8b59f80dce" />
<img width="1920" height="1080" alt="Screenshot-9" src="https://github.com/user-attachments/assets/b76ddccd-d9e5-425e-9d7a-8a08b4181557" />
<img width="1920" height="1080" alt="Screenshot-10" src="https://github.com/user-attachments/assets/a00d0353-cbb6-42b2-bf65-6aa52da1c8da" />
<img width="1920" height="1080" alt="Screenshot-11" src="https://github.com/user-attachments/assets/9505247b-2c45-4414-bc70-06c2335bdd6d" />
<img width="1920" height="1080" alt="Screenshot-12" src="https://github.com/user-attachments/assets/d1a9f349-fb59-4593-b4d6-e82a45686359" />
<img width="1920" height="1080" alt="Screenshot-16" src="https://github.com/user-attachments/assets/8f063a4c-5d6b-4688-ae0a-8179ce152121" />
<img width="1920" height="1080" alt="Screenshot-13" src="https://github.com/user-attachments/assets/0e282520-76dd-4a1a-94b0-ef81f63a5ef2" />
<img width="1920" height="1080" alt="Screenshot-14" src="https://github.com/user-attachments/assets/d102b98a-34a5-4cf0-8056-5e1b4f9b1f20" />
<img width="1920" height="1080" alt="Screenshot-15" src="https://github.com/user-attachments/assets/786cb22d-97c7-4128-8a43-045b0a4334fa" />
<img width="1920" height="1080" alt="Screenshot-17" src="https://github.com/user-attachments/assets/380ace80-06b1-4893-9016-1fdbd3c3e68d" />
<img width="1920" height="1080" alt="Screenshot-18 0" src="https://github.com/user-attachments/assets/18ff6365-6170-4e93-9da3-48a9bf80b098" />
<img width="1920" height="1080" alt="Screenshot-18 1" src="https://github.com/user-attachments/assets/b54dc7cc-a97e-45ae-bbd3-6dc07b300263" />
<img width="1920" height="1080" alt="Screenshot-18 2" src="https://github.com/user-attachments/assets/d81889f8-9cce-4931-aced-2750dee504c0" />
<img width="1920" height="1080" alt="Screenshot-19" src="https://github.com/user-attachments/assets/a7ef6817-c3d0-4e0b-937e-e0047adcb98d" />
<img width="1920" height="1080" alt="Screenshot-20" src="https://github.com/user-attachments/assets/408dca02-9873-43cb-9405-d993098f0edb" />
<img width="1920" height="1080" alt="Screenshot-21" src="https://github.com/user-attachments/assets/ccb94dd5-6c76-44fa-9073-e99cc8bb0200" />
<img width="1920" height="1080" alt="Screenshot-22" src="https://github.com/user-attachments/assets/a00b2e7e-ffcd-4318-9f0d-136b93f98c30" />
<img width="1920" height="1080" alt="Screenshot-23" src="https://github.com/user-attachments/assets/23dbea16-b30e-4e88-8aad-2388c1b86ba8" />

