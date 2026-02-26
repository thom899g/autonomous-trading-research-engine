"""
Firebase Client for Autonomous Trading Research Engine
Implements the unified nervous system with deterministic data flow
"""
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.firestore_v1.collection import CollectionReference
from typing import Dict, Any, Optional, List, Union
import logging
import json
from datetime import datetime
from dataclasses import asdict
import threading

from config import config

logger = logging.getLogger(__name__)

class FirebaseClient:
    """Unified Firebase client for state management and real-time data"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern to ensure single Firebase instance"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None: