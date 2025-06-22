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
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                conn.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def save_entry(self, date: str, journal: str, intention: str, 
                   dream: str, priorities: str, reflection: str, strategy: str) -> bool:
        """
        Save a new journal entry to the database
        
        Args:
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
                    INSERT INTO entries (date, journal, intention, dream, priorities, reflection, strategy)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (date, journal, intention, dream, priorities, reflection, strategy))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving entry: {e}")
            return False
    
    def get_entry_by_date(self, date: str) -> Optional[Dict]:
        """
        Retrieve an entry by date
        
        Args:
            date (str): Date to search for
            
        Returns:
            Dict: Entry data if found, None otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, date, journal, intention, dream, priorities, reflection, strategy, created_at
                    FROM entries WHERE date = ?
                """, (date,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        'id': row[0],
                        'date': row[1],
                        'journal': row[2],
                        'intention': row[3],
                        'dream': row[4],
                        'priorities': row[5],
                        'reflection': row[6],
                        'strategy': row[7],
                        'created_at': row[8]
                    }
                return None
        except Exception as e:
            print(f"Error retrieving entry: {e}")
            return None
    
    def get_all_entries(self) -> List[Dict]:
        """
        Retrieve all entries from the database
        
        Returns:
            List[Dict]: List of all entries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, date, journal, intention, dream, priorities, reflection, strategy, created_at
                    FROM entries ORDER BY date DESC
                """)
                rows = cursor.fetchall()
                
                entries = []
                for row in rows:
                    entries.append({
                        'id': row[0],
                        'date': row[1],
                        'journal': row[2],
                        'intention': row[3],
                        'dream': row[4],
                        'priorities': row[5],
                        'reflection': row[6],
                        'strategy': row[7],
                        'created_at': row[8]
                    })
                return entries
        except Exception as e:
            print(f"Error retrieving entries: {e}")
            return []
    
    def get_available_dates(self) -> List[str]:
        """
        Get list of all available dates in the database
        
        Returns:
            List[str]: List of dates
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT date FROM entries ORDER BY date DESC")
                rows = cursor.fetchall()
                return [row[0] for row in rows]
        except Exception as e:
            print(f"Error retrieving dates: {e}")
            return []
    
    def delete_entry(self, entry_id: int) -> bool:
        """
        Delete an entry by ID
        
        Args:
            entry_id (int): ID of the entry to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting entry: {e}")
            return False
    
    def entry_exists(self, date: str) -> bool:
        """
        Check if an entry exists for a given date
        
        Args:
            date (str): Date to check
            
        Returns:
            bool: True if entry exists, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM entries WHERE date = ?", (date,))
                count = cursor.fetchone()[0]
                return count > 0
        except Exception as e:
            print(f"Error checking entry existence: {e}")
            return False
    
    def get_database_stats(self) -> Dict:
        """
        Get database statistics
        
        Returns:
            Dict: Database statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM entries")
                total_entries = cursor.fetchone()[0]
                
                cursor.execute("SELECT MIN(date), MAX(date) FROM entries")
                date_range = cursor.fetchone()
                
                return {
                    'total_entries': total_entries,
                    'earliest_date': date_range[0] if date_range[0] else None,
                    'latest_date': date_range[1] if date_range[1] else None
                }
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {'total_entries': 0, 'earliest_date': None, 'latest_date': None} 