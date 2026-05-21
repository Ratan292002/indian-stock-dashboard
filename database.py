import sqlite3
import pandas as pd

# -------------------------------------
# DATABASE CONNECTION
# -------------------------------------

conn = sqlite3.connect(
    "market_terminal.db",
    check_same_thread=False
)

cursor = conn.cursor()

# -------------------------------------
# CREATE WATCHLIST TABLE
# -------------------------------------

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS watchlist (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        stock TEXT,

        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''
)

# -------------------------------------
# CREATE AI REPORTS TABLE
# -------------------------------------

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS ai_reports (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        report_date TEXT,

        market_regime TEXT,

        commentary TEXT
    )
    '''
)

# -------------------------------------
# CREATE OPPORTUNITY TABLE
# -------------------------------------

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS opportunities (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        stock TEXT,

        score INTEGER,

        recommendation TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''
)

conn.commit()

# -------------------------------------
# WATCHLIST FUNCTIONS
# -------------------------------------

def add_to_watchlist(stock):

    cursor.execute(
        '''
        INSERT INTO watchlist(stock)
        VALUES(?)
        ''',
        (stock,)
    )

    conn.commit()

def get_watchlist():

    df = pd.read_sql_query(
        "SELECT * FROM watchlist",
        conn
    )

    return df

# -------------------------------------
# OPPORTUNITY FUNCTIONS
# -------------------------------------

def save_opportunity(
    stock,
    score,
    recommendation
):

    cursor.execute(
        '''
        INSERT INTO opportunities(
            stock,
            score,
            recommendation
        )

        VALUES(?,?,?)
        ''',
        (
            stock,
            score,
            recommendation
        )
    )

    conn.commit()

def get_opportunities():

    df = pd.read_sql_query(
        "SELECT * FROM opportunities",
        conn
    )

    return df
