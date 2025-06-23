"""
Database operations for ConsciousDay Agent
Handles SQLite database operations for storing and retrieving journal entries
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    """
    Manages SQLite database operations for the ConsciousDay Agent
    """
    
    def __init__(self, db_path: str = "entries.db"):
        """
        Initialize database manager
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with the required table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # First, create the table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        date TEXT NOT NULL,
                        journal TEXT,
                        intention TEXT,
                        dream TEXT,
                        priorities TEXT,
                        reflection TEXT,
                        strategy TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Now check if user_id column exists (for existing tables that might not have it)
                try:
                    cursor.execute("PRAGMA table_info(entries)")
                    columns = [column[1] for column in cursor.fetchall()]
                    
                    if 'user_id' not in columns:
                        # Add user_id column to existing table
                        cursor.execute("ALTER TABLE entries ADD COLUMN user_id TEXT")
                        print("Added user_id column to entries table")
                        
                        # Migrate existing entries to have a default user_id
                        # This ensures existing data is preserved
                        cursor.execute("UPDATE entries SET user_id = 'demo' WHERE user_id IS NULL")
                        print("Migrated existing entries to default user")
                except Exception as e:
                    print(f"Error checking/updating table schema: {e}")
                
                conn.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def save_entry(self, user_id: str, date: str, journal: str, intention: str, 
                   dream: str, priorities: str, reflection: str, strategy: str) -> bool:
        """
        Save a new journal entry to the database
        
        Args:
            user_id (str): ID of the user creating the entry
            date (str): Date of the entry
            journal (str): Morning journal text
            intention (str): Daily intention
            dream (str): Dream description
            priorities (str): Top 3 priorities
            reflection (str): AI-generated reflection
            strategy (str): AI-generated strategy
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO entries (user_id, date, journal, intention, dream, priorities, reflection, strategy)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, date, journal, intention, dream, priorities, reflection, strategy))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving entry: {e}")
            return False
    
    def get_entry_by_date(self, user_id: str, date: str) -> Optional[Dict]:
        """
        Retrieve an entry by date for a specific user
        
        Args:
            user_id (str): ID of the user
            date (str): Date to search for
            
        Returns:
            Dict: Entry data if found, None otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, user_id, date, journal, intention, dream, priorities, reflection, strategy, created_at
                    FROM entries WHERE user_id = ? AND date = ?
                """, (user_id, date))
                row = cursor.fetchone()
                
                if row:
                    return {
                        'id': row[0],
                        'user_id': row[1],
                        'date': row[2],
                        'journal': row[3],
                        'intention': row[4],
                        'dream': row[5],
                        'priorities': row[6],
                        'reflection': row[7],
                        'strategy': row[8],
                        'created_at': row[9]
                    }
                return None
        except Exception as e:
            print(f"Error retrieving entry: {e}")
            return None
    
    def get_all_entries(self, user_id: str) -> List[Dict]:
        """
        Retrieve all entries for a specific user
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            List[Dict]: List of all entries for the user
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, user_id, date, journal, intention, dream, priorities, reflection, strategy, created_at
                    FROM entries WHERE user_id = ? ORDER BY date DESC
                """, (user_id,))
                rows = cursor.fetchall()
                
                entries = []
                for row in rows:
                    entries.append({
                        'id': row[0],
                        'user_id': row[1],
                        'date': row[2],
                        'journal': row[3],
                        'intention': row[4],
                        'dream': row[5],
                        'priorities': row[6],
                        'reflection': row[7],
                        'strategy': row[8],
                        'created_at': row[9]
                    })
                return entries
        except Exception as e:
            print(f"Error retrieving entries: {e}")
            return []
    
    def get_available_dates(self, user_id: str) -> List[str]:
        """
        Get list of all available dates for a specific user
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            List[str]: List of dates
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT date FROM entries WHERE user_id = ? ORDER BY date DESC", (user_id,))
                rows = cursor.fetchall()
                return [row[0] for row in rows]
        except Exception as e:
            print(f"Error retrieving dates: {e}")
            return []
    
    def delete_entry(self, user_id: str, entry_id: int) -> bool:
        """
        Delete an entry by ID for a specific user
        
        Args:
            user_id (str): ID of the user
            entry_id (int): ID of the entry to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM entries WHERE user_id = ? AND id = ?", (user_id, entry_id))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting entry: {e}")
            return False
    
    def entry_exists(self, user_id: str, date: str) -> bool:
        """
        Check if an entry exists for a given date and user
        
        Args:
            user_id (str): ID of the user
            date (str): Date to check
            
        Returns:
            bool: True if entry exists, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM entries WHERE user_id = ? AND date = ?", (user_id, date))
                count = cursor.fetchone()[0]
                return count > 0
        except Exception as e:
            print(f"Error checking entry existence: {e}")
            return False
    
    def get_database_stats(self, user_id: str) -> Dict:
        """
        Get database statistics for a specific user
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            Dict: Database statistics for the user
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM entries WHERE user_id = ?", (user_id,))
                total_entries = cursor.fetchone()[0]
                
                cursor.execute("SELECT MIN(date), MAX(date) FROM entries WHERE user_id = ?", (user_id,))
                date_range = cursor.fetchone()
                
                return {
                    'total_entries': total_entries,
                    'earliest_date': date_range[0] if date_range[0] else None,
                    'latest_date': date_range[1] if date_range[1] else None
                }
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {'total_entries': 0, 'earliest_date': None, 'latest_date': None} 