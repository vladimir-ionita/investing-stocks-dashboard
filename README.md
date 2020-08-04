# About
Semi-automatic aggregator for stock investments portfolios divided across multiple stock brokerage accounts.

### Problem
The number of stock brokers is increasing every month, 
frequently dividing the investment portfolio across multiple services.
It gets harder and harder to follow the portfolio and make investments decisions.

### Audience
Although this might not be useful for seasoned investors with big, established portfolios,
it might be quite useful for beginners that have a diversified portfolio
and watch closely the investments they've made.

### Installation
This tool is built as a django web service.

Some knowledge about running python code and django web services is required.

Step-by-step installation:
1. Download the code. 
2. Install the dependencies: `pip install requirements.txt`. If you don't have `pip` installed, you need to install it first.
3. Create the local database: `python manage.py migrate`
4. Create a super user: `python manage.py createsuperuser`
5. Run the server: `python manage.py runserver`
6. Go to `localhost:8000/admin` and log in with the super user you have created at step 4.

## Usage
Stocks Dashboard allows you to manually insert all the trades you've made into a dashboard, for an easy overview.

Beside this, it includes commands that allows you to automatically import stock trades from some services.

### Commands
#### `import_stocks_trades` 
This command allows you to import stock trades from Robinhood.
The way it does it is through Robinhood confirmation emails.
Robinhood sends an email each time you buy or sell a stock.
This tool connects to your email address, finds all the emails from robinhood.com, parses them,
finds the trades and imports them in the database. It will ignore duplicates if you run it multiple times.

To use the command, you must pass the email, the email password and the search criteria as arguments:

`python manage.py import_stock_trades <email address> <email password> "<search criteria>"`

This tool connects to your email through IMAP. Gmail, fortunately, by default, doesn't allow IMAP connections,
as it is considered risky and unsecure. You will have to enable access for "Less secure apps" for this to work.
Google `gmail enable less secure apps` and you'll find a way. Also, if you'll try the script before
enabling "Less secure apps", Gmail will send you an email describing the problem and will show you the way to enable it.

Search criteria must follow the format explained in [RFC3501, Section 6.4.4](https://tools.ietf.org/html/rfc3501#section-6.4.4)

#### `import_stocks_trades_local`
This command allows you to import stock trades from a local file.
The data in the file must be saved in a specific format.
Each line in the file must represent a trade using the following format (keep in mind the datetime format as well):

`<stock symbol>|<BUY or SELL>|<share amount>|<share price>|<total trade price>|<datetime (05/17/2020 10:03:16 EST5EDT)>|<brokerage service>`

To use the command, you must pass the file path as an argument:

`python manage.py import_stock_trades_file <file path>`

### Considerations
All the trades are unique. For two trades to be the same, the following fields must be the same:
- stock symbol (or ticker)
- time of trade
- share price
- total trade amount

If a new trade is tried to be imported and the combination of the above data already exists, it will be ignored. 

### In progress
- Implement access to more email servers (currently only Gmail is supported) 
- Import from CSV
