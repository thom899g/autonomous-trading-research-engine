"""
Configuration Manager for Autonomous Trading Research Engine
Centralizes all environment variables and configuration with validation
"""
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging
from pathlib import Path

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ExchangeConfig:
    """Exchange-specific configuration"""
    name: str
    api_key: str
    secret: str
    sandbox: bool = True
    rate_limit: int = 1000  # ms between requests
    
@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    project_id: str
    private_key: str
    client_email: str
    database_url: Optional[str] = None
    
@dataclass
class TradingConfig:
    """Trading parameters"""
    max_position_size: float = 1000.0
    max_daily_loss: float = 500.0
    risk_per_trade: float = 0.02
    min_volume_threshold: float = 100000.0

class ConfigManager:
    """Centralized configuration management with validation"""
    
    def __init__(self):
        self._validate_environment()
        self.firebase = self._load_firebase_config()
        self.exchanges = self._load_exchange_configs()
        self.trading = TradingConfig()
        
    def _validate_environment(self) -> None:
        """Validate required environment variables"""
        required_vars = [
            'FIREBASE_PROJECT_ID',
            'FIREBASE_PRIVATE_KEY',
            'FIREBASE_CLIENT_EMAIL'
        ]
        
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            error_msg = f"Missing required environment variables: {missing}"
            logger.error(error_msg)
            raise EnvironmentError(error_msg)
            
        logger.info("Environment validation passed")
    
    def _load_firebase_config(self) -> FirebaseConfig:
        """Load and validate Firebase configuration"""
        private_key = os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n')
        
        return FirebaseConfig(
            project_id=os.getenv('FIREBASE_PROJECT_ID'),
            private_key=private_key,
            client_email=os.getenv('FIREBASE_CLIENT_EMAIL'),
            database_url=os.getenv('FIREBASE_DATABASE_URL')
        )
    
    def _load_exchange_configs(self) -> Dict[str, ExchangeConfig]:
        """Load configuration for all enabled exchanges"""
        exchanges = {}
        
        # Example: Load Binance config if available
        binance_key = os.getenv('BINANCE_API_KEY')
        binance_secret = os.getenv('BINANCE_API_SECRET')
        
        if binance_key and binance_secret:
            exchanges['binance'] = ExchangeConfig(
                name='binance',
                api_key=binance_key,
                secret=binance_secret,
                sandbox=os.getenv('ENVIRONMENT', 'development') != 'production'
            )
            logger.info(f"Loaded Binance configuration (sandbox: {exchanges['binance'].sandbox})")
            
        return exchanges
    
    def get_exchange_config(self, exchange_name: str) -> Optional[ExchangeConfig]:
        """Get configuration for specific exchange"""
        return self.exchanges.get(exchange_name)
    
    def validate_trading_limits(self, amount: float, symbol: str) -> bool:
        """Validate trade against configured limits"""
        if amount > self.trading.max_position_size:
            logger.warning(f"Trade amount {amount} exceeds max position size")
            return False
        return True

# Global configuration instance
config = ConfigManager()