# Start Local Server
```bash 
uvicorn main:app --reload
```

# Setting up the Local Database
1. Run the Migration Script
   ```bash
   ./run_migrations.sh
   ```

2. Run the Initial Migration Command
   ```bash
    alembic revision --autogenerate -m "Initial tables"
    ```

3. Apply Migration to the Db
   ```bash
   alembic upgrade head
   ```

4. Start the Server
   ```bash
   uvicorn main:app --reload
   ```