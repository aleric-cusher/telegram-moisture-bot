import sqlite3
from sqlite3 import Connection, Cursor

from datetime import datetime
import time
import os

import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)
import matplotlib.pyplot as plt
import matplotlib.style as style


style.use("ggplot")

filename = 'moisture_data.db'
table_name = 'moisture'
path_to_save = os.getcwd() + "/graphs/"


def delete_graph_img(img_path: str) -> None:
    os.system(f"rm {img_path}")

def connect_db(filename: str=filename) -> tuple[Connection, Cursor]:
    db_conn = sqlite3.connect(filename)
    cur = db_conn.cursor()
    return db_conn, cur

def close_db(db_conn: Connection, cur: Cursor) -> None:
    cur.close()
    db_conn.close()

def _get_data(conn: Connection, cur: Cursor, limit: int=36, table_name: str=table_name) -> list[tuple[int, float, int, int]]:
    cur.execute(f"SELECT * FROM {table_name} ORDER BY unix DESC LIMIT {limit}")
    # (SELECT * FROM Employee ORDER BY ID DESC LIMIT 5) ORDER BY ID ASC;
    data = cur.fetchall()
    return data


def generate_graph(limit: int=36, inc_avg: bool=False) -> str:
    conn, cur = connect_db()
    data = _get_data(conn, cur, limit=limit)
    close_db(conn, cur)

    unixs, vals, mins, maxs = [], [], [], []
    for unix, val, min_v, max_v in data[::-1]:
        unixs.append(unix)
        vals.append(val)
        mins.append(min_v)
        maxs.append(max_v)

    # unixs = unixs[30:]
    unixs = [datetime.fromtimestamp(i).strftime("%m/%d-%H%M")  for i in unixs]

    if inc_avg:
        window = 4
        average_data: list[float] = []
        for ind in range(len(vals) - window + 1):
            average_data.append(sum(vals[ind:ind+window])/window)
        plt.plot(unixs[window-1:], average_data, "y")

    plt.plot(unixs, vals, "go-", linewidth=1.3, markersize=2)
    plt.plot(unixs, mins, 'b', linestyle='dotted', linewidth=1.3)
    plt.plot(unixs, maxs, 'r', linestyle='dotted', linewidth=1.3)
    plt.tight_layout()

    img_name = time.strftime("%a_%Y_%H_%M_%S_%I")
    path_to_image = f"{path_to_save}{img_name}.png"
    plt.savefig(path_to_image)
    plt.close()
    return path_to_image


def get_recent_entries(limit: int=4) -> str:
    conn, cur = connect_db()
    data = _get_data(conn, cur, limit=limit)
    close_db(conn, cur)

    data_list: list[str] = []
    for unix, val, min_v, max_v in data:
        time_str = datetime.fromtimestamp(unix).strftime("%b%d %H:%M")
        data_list.append(f"{time_str}-> {val} | {min_v} | {max_v}")
    
    return '\n'.join(data_list)
    
