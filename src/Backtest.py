!pip install lumibot
from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy

# A Three_Candle strategy that buys GOOG 
class Three_Candle(Strategy):
    data = []
    order_number = 0
    def initialize(self):
        self.sleeptime = "1D"


    def on_trading_iteration(self):
        symbol ="GOOG"
        entry_price = self.get_last_price(symbol)
        self.log_message(f"Position: {self.get_position(symbol)}")
        self.data.append(self.get_last_price(symbol))

        if len(self.data) > 3:
            temp = self.data[-3:]
            if temp[-1] > temp[1] > temp[0]:
                self.log_message(f"Last 3 prints: {temp}")
                order = self.create_order(symbol, quantity = 10, side = "buy")
                self.submit_order(order)
                self.order_number += 1
                if self.order_number == 1:
                    self.log_message(f"Entry price: {temp[-1]}")
                    entry_price = temp[-1]  
            if self.get_position(symbol) and self.data[-1] < entry_price * .995:
                self.sell_all()
                self.order_number = 0
            elif self.get_position(symbol) and self.data[-1] >= entry_price * 1.015:
                self.sell_all()
                self.order_number = 0
    def before_market_closes(self):
        self.sell_all()

# Pick the dates that you want to start and end your backtest
# and the allocated budget
backtesting_start = datetime(2020, 11, 1)
backtesting_end = datetime(2020, 12, 31)

# Run the backtest
Three_Candle.backtest(
    YahooDataBacktesting,
    backtesting_start,
    backtesting_end,
)
