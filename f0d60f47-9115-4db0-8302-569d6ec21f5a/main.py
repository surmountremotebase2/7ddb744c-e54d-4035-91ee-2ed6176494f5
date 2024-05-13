from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        """
        Initialize the TradingStrategy class by defining the asset tickers
        you are interested in. Here, we're only interested in 'AAPL'.
        """
        self.ticker = "AAPL"

    @property
    def assets(self):
        """
        Define the assets this strategy will use. This can be a list of tickers.
        In our case, it's just one ticker, 'AAPL'.
        """
        return [self.ticker]

    @property
    def interval(self):
        """
        Define the time interval for the trading signals. Here we use '1day' 
        for daily trading signals.
        """
        return "1day"

    def run(self, data):
        """
        The core logic of the trading strategy implemented here.
        We check the RSI for the 'AAPL' stock and decide whether to go long
        (buy) or short (sell) based on the RSI oversold and overbought conditions.
        """
        # Calculate the RSI for AAPL with a look-back period of 14 days
        rsi_values = RSI(self.ticker, data["ohlcv"], length=14)
        
        # Initialize AAPL stake to 0
        aapl_stake = 0

        # Check if we have enough data points for the RSI calculation
        if rsi_values and len(rsi_values) > 0:
            # Get the latest RSI value
            latest_rsi = rsi_values[-1]
            
            # Define the RSI thresholds for oversold and overbought conditions
            oversold_threshold = 30
            overbought_threshold = 70
            
            # If the RSI indicates that AAPL is oversold, we go long (buy).
            if latest_rsi < oversold_threshold:
                aapl_stake = 1  # Represent a 100% allocation
            
            # If the RSI indicates that AAPL is overbought, we sell it off by setting its allocation to 0.
            elif latest_rsi > overbought_threshold:
                aapl_stake = 0  # Represent a 0% allocation
                
        # Return our target allocations based on RSI analysis
        return TargetAllocation({self.ticker: aapl_stake})