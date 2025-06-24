"""
Database operations for ConsciousDay Agent
Handles SQLite database operations for storing and retrieving journal entries
"""

import sqlite3
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, date)
                    )
                """)
                
                # Now check if user_id column exists (for existing tables that might not have it)
                try:
                    cursor.execute("PRAGMA table_info(entries)")
                    columns = [column[1] for column in cursor.fetchall()]
                    
                    if 'user_id' not in columns:
                        # Add user_id column to existing table
                        cursor.execute("ALTER TABLE entries ADD COLUMN user_id TEXT")
                        logger.info("Added user_id column to entries table")
                        
                        # Migrate existing entries to have a default user_id
                        # This ensures existing data is preserved
                        cursor.execute("UPDATE entries SET user_id = 'demo' WHERE user_id IS NULL")
                        logger.info("Migrated existing entries to default user")
                        
                        # Add unique constraint after migration
                        try:
                            cursor.execute("CREATE UNIQUE INDEX idx_user_date ON entries(user_id, date)")
                            logger.info("Added unique constraint on user_id and date")
                        except sqlite3.IntegrityError:
                            logger.warning("Could not add unique constraint - duplicate entries may exist")
                            
                except Exception as e:
                    logger.error(f"Error checking/updating table schema: {e}")
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def _validate_inputs(self, user_id: str, date: str, **kwargs) -> bool:
        """
        Validate input parameters
        
        Args:
            user_id (str): User ID to validate
            date (str): Date to validate
            **kwargs: Additional parameters to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not user_id or not user_id.strip():
            logger.error("user_id is required and cannot be empty")
            return False
        
        if not date or not date.strip():
            logger.error("date is required and cannot be empty")
            return False
        
        # Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            logger.error(f"Invalid date format: {date}. Expected YYYY-MM-DD")
            return False
        
        return True
    
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
        # Validate inputs
        if not self._validate_inputs(user_id, date):
            return False
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if entry already exists
                cursor.execute("SELECT id FROM entries WHERE user_id = ? AND date = ?", (user_id, date))
                existing = cursor.fetchone()
                
                if existing:
                    logger.warning(f"Entry already exists for user {user_id} on date {date}")
                    return False
                
                cursor.execute("""
                    INSERT INTO entries (user_id, date, journal, intention, dream, priorities, reflection, strategy)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, date, journal, intention, dream, priorities, reflection, strategy))
                conn.commit()
                
                logger.info(f"Successfully saved entry for user {user_id} on date {date}")
                return True
                
        except sqlite3.IntegrityError as e:
            logger.error(f"Integrity error saving entry: {e}")
            return False
        except Exception as e:
            logger.error(f"Error saving entry: {e}")
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
        # Validate inputs
        if not self._validate_inputs(user_id, date):
            return None
        
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
            logger.error(f"Error retrieving entry: {e}")
            return None
    
    def get_all_entries(self, user_id: str) -> List[Dict]:
        """
        Retrieve all entries for a specific user
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            List[Dict]: List of all entries for the user
        """
        if not user_id or not user_id.strip():
            logger.error("user_id is required and cannot be empty")
            return []
        
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
            logger.error(f"Error retrieving entries: {e}")
            return []
    
    def get_available_dates(self, user_id: str) -> List[str]:
        """
        Get list of all available dates for a specific user
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            List[str]: List of dates
        """
        if not user_id or not user_id.strip():
            logger.error("user_id is required and cannot be empty")
            return []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT date FROM entries WHERE user_id = ? ORDER BY date DESC", (user_id,))
                rows = cursor.fetchall()
                return [row[0] for row in rows]
                
        except Exception as e:
            logger.error(f"Error retrieving dates: {e}")
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
        if not user_id or not user_id.strip():
            logger.error("user_id is required and cannot be empty")
            return False
        
        if not isinstance(entry_id, int) or entry_id <= 0:
            logger.error("entry_id must be a positive integer")
            return False
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM entries WHERE user_id = ? AND id = ?", (user_id, entry_id))
                conn.commit()
                
                if cursor.rowcount > 0:
                    logger.info(f"Successfully deleted entry {entry_id} for user {user_id}")
                    return True
                else:
                    logger.warning(f"No entry found with id {entry_id} for user {user_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error deleting entry: {e}")
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
        # Validate inputs
        if not self._validate_inputs(user_id, date):
            return False
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM entries WHERE user_id = ? AND date = ?", (user_id, date))
                count = cursor.fetchone()[0]
                return count > 0
                
        except Exception as e:
            logger.error(f"Error checking entry existence: {e}")
            return False
    
    def get_database_stats(self, user_id: str) -> Dict:
        """
        Get database statistics for a specific user
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            Dict: Database statistics for the user
        """
        if not user_id or not user_id.strip():
            logger.error("user_id is required and cannot be empty")
            return {'total_entries': 0, 'earliest_date': None, 'latest_date': None}
        
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
            logger.error(f"Error getting database stats: {e}")
            return {'total_entries': 0, 'earliest_date': None, 'latest_date': None}
    
    def update_entry(self, user_id: str, entry_id: int, **kwargs) -> bool:
        """
        Update an existing entry
        
        Args:
            user_id (str): ID of the user
            entry_id (int): ID of the entry to update
            **kwargs: Fields to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not user_id or not user_id.strip():
            logger.error("user_id is required and cannot be empty")
            return False
        
        if not isinstance(entry_id, int) or entry_id <= 0:
            logger.error("entry_id must be a positive integer")
            return False
        
        if not kwargs:
            logger.error("No fields to update")
            return False
        
        # Validate allowed fields
        allowed_fields = {'journal', 'intention', 'dream', 'priorities', 'reflection', 'strategy'}
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            logger.error("No valid fields to update")
            return False
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build update query
                set_clause = ", ".join([f"{field} = ?" for field in update_fields.keys()])
                query = f"UPDATE entries SET {set_clause} WHERE user_id = ? AND id = ?"
                
                values = list(update_fields.values()) + [user_id, entry_id]
                cursor.execute(query, values)
                conn.commit()
                
                if cursor.rowcount > 0:
                    logger.info(f"Successfully updated entry {entry_id} for user {user_id}")
                    return True
                else:
                    logger.warning(f"No entry found with id {entry_id} for user {user_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error updating entry: {e}")
            return False 