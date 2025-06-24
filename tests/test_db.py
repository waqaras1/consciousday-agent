"""
Database tests for ConsciousDay Agent
Tests for database operations
"""

import pytest
import os
import tempfile
from database.db_operations import DatabaseManager

class TestDatabaseManager:
    """Test cases for DatabaseManager class"""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        yield db_path
        
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    @pytest.fixture
    def db_manager(self, temp_db):
        """Create a DatabaseManager instance with temporary database"""
        return DatabaseManager(temp_db)
    
    def test_init_database(self, db_manager):
        """Test database initialization"""
        # Check if table exists
        import sqlite3
        with sqlite3.connect(db_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entries'")
            result = cursor.fetchone()
            assert result is not None
    
    def test_save_entry(self, db_manager):
        """Test saving an entry"""
        success = db_manager.save_entry(
            user_id="test_user",
            date="2024-01-01",
            journal="Test journal entry",
            intention="Test intention",
            dream="Test dream",
            priorities="1. Test priority 1\n2. Test priority 2\n3. Test priority 3",
            reflection="Test reflection",
            strategy="Test strategy"
        )
        assert success is True
    
    def test_get_entry_by_date(self, db_manager):
        """Test retrieving an entry by date"""
        # Save an entry first
        db_manager.save_entry(
            user_id="test_user",
            date="2024-01-01",
            journal="Test journal entry",
            intention="Test intention",
            dream="Test dream",
            priorities="1. Test priority 1\n2. Test priority 2\n3. Test priority 3",
            reflection="Test reflection",
            strategy="Test strategy"
        )
        
        # Retrieve the entry
        entry = db_manager.get_entry_by_date("test_user", "2024-01-01")
        assert entry is not None
        assert entry['date'] == "2024-01-01"
        assert entry['journal'] == "Test journal entry"
        assert entry['intention'] == "Test intention"
    
    def test_get_entry_by_date_not_found(self, db_manager):
        """Test retrieving an entry that doesn't exist"""
        entry = db_manager.get_entry_by_date("test_user", "2024-01-01")
        assert entry is None
    
    def test_get_all_entries(self, db_manager):
        """Test retrieving all entries"""
        # Save multiple entries
        db_manager.save_entry(
            user_id="test_user",
            date="2024-01-01",
            journal="Entry 1",
            intention="Intention 1",
            dream="Dream 1",
            priorities="Priorities 1",
            reflection="Reflection 1",
            strategy="Strategy 1"
        )
        
        db_manager.save_entry(
            user_id="test_user",
            date="2024-01-02",
            journal="Entry 2",
            intention="Intention 2",
            dream="Dream 2",
            priorities="Priorities 2",
            reflection="Reflection 2",
            strategy="Strategy 2"
        )
        
        entries = db_manager.get_all_entries("test_user")
        assert len(entries) == 2
        assert entries[0]['date'] == "2024-01-02"  # Should be sorted by date DESC
        assert entries[1]['date'] == "2024-01-01"
    
    def test_get_available_dates(self, db_manager):
        """Test getting available dates"""
        # Save entries
        db_manager.save_entry(
            user_id="test_user",
            date="2024-01-01",
            journal="Entry 1",
            intention="Intention 1",
            dream="Dream 1",
            priorities="Priorities 1",
            reflection="Reflection 1",
            strategy="Strategy 1"
        )
        
        db_manager.save_entry(
            user_id="test_user",
            date="2024-01-02",
            journal="Entry 2",
            intention="Intention 2",
            dream="Dream 2",
            priorities="Priorities 2",
            reflection="Reflection 2",
            strategy="Strategy 2"
        )
        
        dates = db_manager.get_available_dates("test_user")
        assert len(dates) == 2
        assert "2024-01-01" in dates
        assert "2024-01-02" in dates
    
    def test_delete_entry(self, db_manager):
        """Test deleting an entry"""
        # Save an entry first
        db_manager.save_entry(
            user_id="test_user",
            date="2024-01-01",
            journal="Test journal entry",
            intention="Test intention",
            dream="Test dream",
            priorities="Priorities",
            reflection="Reflection",
            strategy="Strategy"
        )
        
        # Get the entry to get its ID
        entry = db_manager.get_entry_by_date("test_user", "2024-01-01")
        entry_id = entry['id']
        
        # Delete the entry
        success = db_manager.delete_entry("test_user", entry_id)
        assert success is True
        
        # Verify it's deleted
        entry_after_delete = db_manager.get_entry_by_date("test_user", "2024-01-01")
        assert entry_after_delete is None
    
    def test_entry_exists(self, db_manager):
        """Test checking if an entry exists"""
        # Initially no entry exists
        assert db_manager.entry_exists("test_user", "2024-01-01") is False
        
        # Save an entry
        db_manager.save_entry(
            user_id="test_user",
            date="2024-01-01",
            journal="Test journal entry",
            intention="Test intention",
            dream="Test dream",
            priorities="Priorities",
            reflection="Reflection",
            strategy="Strategy"
        )
        
        # Now entry should exist
        assert db_manager.entry_exists("test_user", "2024-01-01") is True
    
    def test_get_database_stats(self, db_manager):
        """Test getting database statistics"""
        # Initially empty database
        stats = db_manager.get_database_stats("test_user")
        assert stats['total_entries'] == 0
        assert stats['earliest_date'] is None
        assert stats['latest_date'] is None
        
        # Add entries
        db_manager.save_entry(
            user_id="test_user",
            date="2024-01-01",
            journal="Entry 1",
            intention="Intention 1",
            dream="Dream 1",
            priorities="Priorities 1",
            reflection="Reflection 1",
            strategy="Strategy 1"
        )
        
        db_manager.save_entry(
            user_id="test_user",
            date="2024-01-02",
            journal="Entry 2",
            intention="Intention 2",
            dream="Dream 2",
            priorities="Priorities 2",
            reflection="Reflection 2",
            strategy="Strategy 2"
        )
        
        stats = db_manager.get_database_stats("test_user")
        assert stats['total_entries'] == 2
        assert stats['earliest_date'] == "2024-01-01"
        assert stats['latest_date'] == "2024-01-02"
    
    def test_user_isolation(self, db_manager):
        """Test that users can only see their own entries"""
        # Save entries for two different users
        db_manager.save_entry(
            user_id="user1",
            date="2024-01-01",
            journal="User 1 entry",
            intention="User 1 intention",
            dream="User 1 dream",
            priorities="User 1 priorities",
            reflection="User 1 reflection",
            strategy="User 1 strategy"
        )
        
        db_manager.save_entry(
            user_id="user2",
            date="2024-01-01",
            journal="User 2 entry",
            intention="User 2 intention",
            dream="User 2 dream",
            priorities="User 2 priorities",
            reflection="User 2 reflection",
            strategy="User 2 strategy"
        )
        
        # User 1 should only see their own entries
        user1_entries = db_manager.get_all_entries("user1")
        assert len(user1_entries) == 1
        assert user1_entries[0]['journal'] == "User 1 entry"
        
        # User 2 should only see their own entries
        user2_entries = db_manager.get_all_entries("user2")
        assert len(user2_entries) == 1
        assert user2_entries[0]['journal'] == "User 2 entry"

if __name__ == "__main__":
    pytest.main([__file__]) 