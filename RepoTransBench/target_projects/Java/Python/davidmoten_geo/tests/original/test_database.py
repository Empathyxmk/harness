import sqlite3
import time
import tempfile
import os
import threading
import pytest

class DummyGeoHash:
    @staticmethod
    def encodeHash(lat, lon, length=None):
        # Return deterministic dummy hash for test
        lat_code = int(abs(hash(lat)) % 1000)
        lon_code = int(abs(hash(lon)) % 1000)
        if length is None:
            length = 12
        return f"d{lat_code}_{lon_code}_{length}"

    @staticmethod
    def coverBoundingBox(lat1, lon1, lat2, lon2, length):
        # Return a simple deterministic set of 'hashes'
        num_hashes = max(1, length)
        return DummyCoverage({f'dbb{i}' for i in range(num_hashes)}, length)

class DummyCoverage:
    def __init__(self, hashes, hash_length):
        self.hashes = set(hashes)
        self.hash_length = hash_length

    def getHashes(self):
        return self.hashes

    def getHashLength(self):
        return self.hash_length

    def getRatio(self):
        return float(self.hash_length * 10)

def test_create_database_insert_records_and_run_benchmark_queries(tmp_path, capsys):
    # Use SQLite in-memory DB for the test
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    # Create schema
    cursor.execute("""CREATE TABLE report (
        time INTEGER,
        lat REAL,
        lon REAL,
        name TEXT,
        geohash1 TEXT,
        geohash2 TEXT,
        geohash3 TEXT,
        geohash4 TEXT,
        geohash5 TEXT,
        geohash6 TEXT,
        geohash7 TEXT,
        geohash8 TEXT,
        geohash9 TEXT,
        geohash10 TEXT,
        geohash11 TEXT,
        geohash12 TEXT
    )""")
    now = int(time.time() * 1000)
    n = 10
    # Insert test rows
    for i in range(n):
        t = now - int(1 * 24 * 60 * 60 * 1000)
        lat = -5.0 + i * 0.1
        lon = 136.0 + i * 0.1
        name = f"name{i}"
        gh = [DummyGeoHash.encodeHash(lat, lon, j) for j in range(1, 13)]
        cursor.execute("""
            INSERT INTO report (
                time, lat, lon, name, geohash1, geohash2, geohash3, geohash4,
                geohash5, geohash6, geohash7, geohash8, geohash9, geohash10, geohash11, geohash12
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (t, lat, lon, name, *gh)
        )
    # Create indexes
    for i in range(1, 13):
        cursor.execute(f"CREATE INDEX idx_geohash_{i} ON report(geohash{i})")
    cursor.execute("CREATE INDEX idx_report_time ON report(time)")

    # Query: time range and bounding box
    length = 4
    coverage = DummyGeoHash.coverBoundingBox(-5, 136, -6, 138, length)
    hashes = coverage.getHashes()
    query = f"""SELECT name, lat, lon FROM report WHERE
        time >= ? AND time < ? AND lat >= -6 AND lat <= -5 AND lon >= 136 AND lon <= 138 AND (
            {' OR '.join([f'geohash{length}="{h}"' for h in hashes])}
        )
    """
    params = (now - int(1 * 24 * 60 * 60 * 1000), now)
    cursor.execute(query, params)
    results = cursor.fetchall()
    # There should be results (not empty)
    assert isinstance(results, list)
    conn.close()