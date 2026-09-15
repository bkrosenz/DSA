import time
from threading import RLock, Thread, Event
from typing import Any, Dict, Optional, Tuple


class KVStore(object):
    """
    Thread-safe KV store with time-to-live, zero memory leaks, and automatic TTL cleanup.
    """

    def __init__(self, default_ttl: Optional[float] = None, auto_cleanup_interval: Optional[float] = None):
        self._lock = RLock()
        self._store: Dict[str, Tuple[Any, Optional[float]]] = {}

        self._stop_cleanup = Event()
        self._cleanup_thread: Optional[Thread] = None

        self._default_ttl = default_ttl

        if auto_cleanup_interval and auto_cleanup_interval > 0:
            self.start_background_cleanup(auto_cleanup_interval)

    def _current_time(self) -> float:
        """Return the current monotonic time to prevent clock shift issues."""
        return time.monotonic()

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return default
            value, expiry = entry
            if expiry is not None and self._current_time() >= expiry:
                del self._store[key]
                return default
            return value

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Set a key with optional TTL (automatically overwrites previous TTL)."""
        true_ttl = ttl if ttl is not None else self._default_ttl
        if true_ttl is not None and true_ttl > 0:
            expiry = self._current_time() + true_ttl
        else:
            expiry = None
        with self._lock:
            self._store[key] = (value, expiry)

    def delete(self, key: str) -> bool:
        """Delete a key from the store. Returns True if present, False otherwise."""
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    def pop(self, key: str, default: Any = None) -> Any:
        """Remove and return the value for key if present, else default."""
        with self._lock:
            val = self.get(key, default=default)
            if key in self._store:
                self.delete(key)
                return val
            return default

    def contains(self, key: str) -> bool:
        """Check if a non-expired key exists in the store."""
        with self._lock:
            return self.get(key) is not None

    def __contains__(self, key: str) -> bool:
        return self.contains(key)

    def get_range(
        self,
        start_key: Optional[str] = None,
        end_key: Optional[str] = None,
        include_start: bool = True,
        include_end: bool = True,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Return a dictionary of key-value pairs for non-expired keys falling within 
        the specified lexicographical range [start_key, end_key]. Results are sorted by key.
        """
        now = self._current_time()
        result = {}
        with self._lock:
            expired = []
            for key in sorted(self._store.keys()):
                value, expiry = self._store[key]

                # Purge and skip expired entries
                if expiry is not None and now >= expiry:
                    expired.append(key)
                    continue

                # Start key filter
                if start_key is not None:
                    if include_start and key < start_key:
                        continue
                    elif not include_start and key <= start_key:
                        continue

                # End key filter
                if end_key is not None:
                    if include_end and key > end_key:
                        continue
                    elif not include_end and key >= end_key:
                        continue

                result[key] = value
                if limit is not None and len(result) >= limit:
                    break

            for key in expired:
                del self._store[key]

        return result

    def get_by_prefix(self, prefix: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Return a dictionary of non-expired key-value pairs where keys start with the given prefix.
        Results are sorted by key.
        """
        now = self._current_time()
        result = {}
        with self._lock:
            expired = []
            for key in sorted(self._store.keys()):
                value, expiry = self._store[key]

                if expiry is not None and now >= expiry:
                    expired.append(key)
                    continue

                if key.startswith(prefix):
                    result[key] = value
                    if limit is not None and len(result) >= limit:
                        break

            for key in expired:
                del self._store[key]

        return result

    def cleanup_expired(self) -> int:
        """
        Active Purge: Scan and remove all expired keys from memory.
        Returns the number of keys purged.
        """
        now = self._current_time()
        expired = []
        with self._lock:
            for key, (_, expiry) in self._store.items():
                if expiry is not None and now >= expiry:
                    expired.append(key)
            for key in expired:
                del self._store[key]
        return len(expired)

    def size(self) -> int:
        """Return the count of active (non-expired) keys."""
        with self._lock:
            self.cleanup_expired()
            return len(self._store)

    def __len__(self) -> int:
        return self.size()

    def clear(self) -> None:
        """Remove all entries from the store."""
        with self._lock:
            self._store.clear()

    def start_background_cleanup(self, interval: float) -> None:
        """Start a background daemon thread to purge unaccessed expired keys periodically."""
        with self._lock:
            if self._cleanup_thread and self._cleanup_thread.is_alive():
                return
            
            # Reset event signal before launching new thread
            self._stop_cleanup.clear()

            def _worker():
                while not self._stop_cleanup.wait(interval):
                    self.cleanup_expired()

            self._cleanup_thread = Thread(
                target=_worker, 
                name='KVStore-CleanupDaemon',
                daemon=True
            )
            # Start the thread
            self._cleanup_thread.start()

    def stop_background_cleanup(self) -> None:
        """Stop the background cleanup thread gracefully."""
        with self._lock:
            if self._cleanup_thread:
                self._stop_cleanup.set()
                self._cleanup_thread = None

    def close(self) -> None:
        """Stop background tasks and clear resources."""
        self.stop_background_cleanup()
        self.clear()
    
    def get_range(
            self,
            start_key: Optional[str] = None,
            end_key: Optional[str] = None,
            include_start: bool = True,
            include_end: bool = True,
            limit: Optional[int] = None
        ) -> Dict[str, Any]:
            """
            Return a dictionary of key-value pairs for non-expired keys falling within 
            the specified lexicographical range. Results are sorted by key.
            """
            with self._lock:
                self.cleanup_expired()
                
                # First filter and sort the keys
                sorted_keys = sorted(self._store.keys())
                
                items = []
                for k in sorted_keys:
                    # Apply start_key filter
                    if start_key is not None:
                        if include_start and k < start_key:
                            continue
                        elif not include_start and k <= start_key:
                            continue
                            
                    # Apply end_key filter
                    if end_key is not None:
                        if include_end and k > end_key:
                            continue
                        elif not include_end and k >= end_key:
                            continue
                            
                    # If it passes filters, add to items
                    v, _ = self._store[k]
                    items.append((k, v))
                    
                    if limit is not None and len(items) >= limit:
                        break
                        
                return dict(items)


    def get_by_prefix(self, prefix: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Return a dictionary of non-expired key-value pairs where keys start with the given prefix.
        Results are sorted by key.
        """
        with self._lock:
            self.cleanup_expired() # O(n)
            
            # Sort first so the limit cuts off the correctly sorted elements
            sorted_keys = sorted(self._store.keys())
            
            items = []
            for k in sorted_keys:
                if k.startswith(prefix):
                    v, _ = self._store[k]
                    items.append((k, v))
                    if limit is not None and len(items) >= limit:
                        break
            return dict(items)