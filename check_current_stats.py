import sqlite3
import datetime

db_path = "/app/nofx-stack/nofx/data/data.db"

def get_stats():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get latest equity
    try:
        query_equity = "SELECT total_equity, created_at FROM trader_equity_snapshots ORDER BY created_at DESC LIMIT 1"
        cursor.execute(query_equity)
        row = cursor.fetchone()
        if row:
            current_equity = row[0]
            last_update = row[1]
        else:
            current_equity = 0
            last_update = 0
    except Exception as e:
        print(f"Error getting equity: {e}")
        current_equity = 0

    # Calculate Win Rate & Profit Factor from positions (closed)
    # 2026-01-27 00:00:00 UTC = 1769472000000 ms
    start_ts = 1769472000000
    
    query_positions = "SELECT realized_pnl, fee, status, close_reason, created_at FROM trader_positions WHERE status = 'CLOSED' AND created_at >= ?"
    cursor.execute(query_positions, (start_ts,))
    rows = cursor.fetchall()
    
    conn.close()
    
    if not rows:
        return current_equity, 0, 0, 0, []

    # Calculate stats
    wins_pnl = 0
    losses_pnl = 0
    win_count = 0
    net_pnls = []
    
    # Sort by created_at (last element in row)
    sorted_rows = sorted(rows, key=lambda x: x[4], reverse=True)
    
    # Calculate daily/recent stats for comparison
    recent_wins = 0
    recent_total = 0
    # Last 48h (approx 2 days)
    # 2 days ms = 172800000
    cutoff_48h = sorted_rows[0][4] - 172800000 if sorted_rows else 0
    
    for row in sorted_rows:
        realized_pnl = row[0] if row[0] is not None else 0
        fee = row[1] if row[1] is not None else 0
        timestamp = row[4]
        
        # net_pnl = realized_pnl - fee
        net_pnl = realized_pnl - fee
        net_pnls.append(net_pnl)
        
        is_win = net_pnl > 0
        if is_win:
            wins_pnl += net_pnl
            win_count += 1
        else:
            losses_pnl += abs(net_pnl)
            
        if timestamp >= cutoff_48h:
            recent_total += 1
            if is_win:
                recent_wins += 1
            
    total_trades = len(rows)
    win_rate = (win_count / total_trades) * 100 if total_trades > 0 else 0
    
    recent_win_rate = (recent_wins / recent_total) * 100 if recent_total > 0 else 0
    print(f"RECENT_48H_WIN_RATE:{recent_win_rate:.2f}")

    profit_factor = wins_pnl / losses_pnl if losses_pnl > 0 else float('inf')
    
    # Recent 10 trades PnL
    recent_pnl = net_pnls[:10]
    
    # Print timestamps
    if sorted_rows:
        last_trade_time = sorted_rows[0][4]
        first_trade_time = sorted_rows[-1][4]
        print(f"FIRST_TRADE_TS:{first_trade_time}")
        print(f"LAST_TRADE_TS:{last_trade_time}")
    
    return current_equity, win_rate, profit_factor, total_trades, recent_pnl

if __name__ == "__main__":
    equity, wr, pf, count, recent = get_stats()
    print(f"EQUITY:{equity}")
    print(f"WIN_RATE:{wr:.2f}")
    print(f"PROFIT_FACTOR:{pf:.2f}")
    print(f"TOTAL_TRADES:{count}")
    print(f"RECENT_PNL:{recent}")
