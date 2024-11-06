import pytest
from django.core.management import call_command
from django.db import connection


@pytest.fixture(autouse=True)
def reset_db_after_test():
    # This runs before each test, clearing the database
    call_command('flush', '--no-input', verbosity=0)
    call_command('migrate', verbosity=0)

    # Reset the auto-incrementing ID sequences for all tables that have an 'id' column
    with connection.cursor() as cursor:
        cursor.execute("""
            DO $$
            DECLARE
                r RECORD;
            BEGIN
                -- Loop through all tables in the public schema
                FOR r IN 
                    SELECT tablename
                    FROM pg_tables
                    WHERE schemaname = 'public' 
                    AND EXISTS (SELECT 1 FROM information_schema.columns 
                    WHERE table_name = pg_tables.tablename AND column_name = 'id') 
                LOOP
                    -- Reset the sequence for each table that has an 'id' column
                    EXECUTE 'SELECT setval(pg_get_serial_sequence(''' || r.tablename || ''', ''id''), 1, false)';
                END LOOP;
            END;
            $$;
        """)
    yield

