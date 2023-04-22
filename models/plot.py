import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def format_data(symbol, data):
	# Formats a bars object as a dataframe for plotting
	df = pd.DataFrame(data['bars'][symbol])
	df['timestamp'] = pd.to_datetime(df['t'], utc=True)
	df.set_index('timestamp', inplace=True)
	df.rename(columns={'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close', 'v': 'Volume'}, inplace=True)
	return df
	
	
def plot_df(symbol, df):
	# Plots a converted bars object as OHLC chart
	fig, ax = plt.subplots()
	ax.set_title(f'{symbol} OHLC Chart')
	ax.set_xlabel('Date')
	ax.set_ylabel('Price')
	# Set the x-axis to display dates
	ax.xaxis_date()
	# Plot the candlesticks
	candlesticks = zip(mdates.date2num(df.index.to_pydatetime()), df['Open'], df['High'], df['Low'], df['Close'])
	for candlestick in candlesticks:
		ax.plot([candlestick[0], candlestick[0]], [candlestick[1], candlestick[2]], color='black')
		ax.plot([candlestick[0], candlestick[0]], [candlestick[3], candlestick[4]], color='black')
		if candlestick[4] > candlestick[1]:
			ax.fill_between([candlestick[0], candlestick[0]], candlestick[1], candlestick[4], facecolor='green', alpha=0.5)
		else:
			ax.fill_between([candlestick[0], candlestick[0]], candlestick[1], candlestick[4], facecolor='red', alpha=0.5)
			
	# Show the plot
	plt.show()

