"""Backtesting engine for trading strategies"""
import numpy as np
import pandas as pd

class Backtester:
    def __init__(self, initial_capital=10000, transaction_cost=0.001):
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost
        self.reset()
        
    def reset(self):
        """Reset backtester state"""
        self.capital = self.initial_capital
        self.position = 0  # Number of shares held
        self.trades = []
        self.portfolio_values = []
        
    def run_backtest(self, data_with_signals):
        """Run backtest on data with trading signals"""
        self.reset()
        df = data_with_signals.copy()
        
        for idx, row in df.iterrows():
            price = row['close']
            signal = row.get('signal', 0)
            
            # Execute trades based on signals
            if signal == 1 and self.position == 0:  # Buy signal
                shares_to_buy = int(self.capital / (price * (1 + self.transaction_cost)))
                if shares_to_buy > 0:
                    cost = shares_to_buy * price * (1 + self.transaction_cost)
                    self.capital -= cost
                    self.position = shares_to_buy
                    self.trades.append({
                        'date': row.get('date', idx),
                        'type': 'BUY',
                        'price': price,
                        'shares': shares_to_buy,
                        'cost': cost
                    })
                    
            elif signal == -1 and self.position > 0:  # Sell signal
                revenue = self.position * price * (1 - self.transaction_cost)
                self.capital += revenue
                self.trades.append({
                    'date': row.get('date', idx),
                    'type': 'SELL',
                    'price': price,
                    'shares': self.position,
                    'revenue': revenue
                })
                self.position = 0
            
            # Calculate current portfolio value
            portfolio_value = self.capital + (self.position * price)
            self.portfolio_values.append(portfolio_value)
        
        # Close any open position at the end
        if self.position > 0:
            final_price = df.iloc[-1]['close']
            revenue = self.position * final_price * (1 - self.transaction_cost)
            self.capital += revenue
            self.trades.append({
                'date': df.iloc[-1].get('date', len(df)-1),
                'type': 'SELL',
                'price': final_price,
                'shares': self.position,
                'revenue': revenue
            })
            self.position = 0
        
        return self.calculate_metrics()
    
    def calculate_metrics(self):
        """Calculate performance metrics"""
        if not self.portfolio_values:
            return None
        
        portfolio_values = np.array(self.portfolio_values)
        
        # Total return
        final_value = portfolio_values[-1]
        total_return = ((final_value - self.initial_capital) / self.initial_capital) * 100
        
        # Calculate returns
        returns = np.diff(portfolio_values) / portfolio_values[:-1]
        returns = returns[np.isfinite(returns)]  # Remove inf/nan
        
        # Sharpe Ratio (assuming 252 trading days, 0% risk-free rate)
        if len(returns) > 0 and np.std(returns) > 0:
            sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252)
        else:
            sharpe_ratio = 0
        
        # Maximum Drawdown
        cumulative_returns = (portfolio_values / self.initial_capital)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = np.min(drawdown) * 100
        
        # Win/Loss Ratio
        buy_trades = [t for t in self.trades if t['type'] == 'BUY']
        sell_trades = [t for t in self.trades if t['type'] == 'SELL']
        
        wins = 0
        losses = 0
        if len(buy_trades) > 0 and len(sell_trades) > 0:
            for i in range(min(len(buy_trades), len(sell_trades))):
                if sell_trades[i]['price'] > buy_trades[i]['price']:
                    wins += 1
                else:
                    losses += 1
        
        win_rate = (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0
        
        return {
            'initial_capital': self.initial_capital,
            'final_capital': final_value,
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'total_trades': len(self.trades),
            'winning_trades': wins,
            'losing_trades': losses,
            'portfolio_values': portfolio_values,
            'trades': self.trades
        }