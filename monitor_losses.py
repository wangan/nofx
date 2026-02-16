#!/usr/bin/env python3
"""
监控连续亏损记录的脚本
"""

import sqlite3
import os

def get_consecutive_losses(db_path):
    """
    从数据库中获取连续亏损的记录
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查询所有已平仓的交易
        cursor.execute("""
            SELECT realized_pnl
            FROM trader_positions
            WHERE trader_id = 'e9d25a69_a8108275-8e41-448c-ba17-6414744cc62a_deepseek_1766223494'
              AND status = 'CLOSED'
            ORDER BY exit_time DESC
        """)
        
        trades = cursor.fetchall()
        
        # 计算连续亏损的最大次数
        max_consecutive_losses = 0
        current_consecutive_losses = 0
        
        for trade in trades:
            pnl = trade[0]
            if pnl < 0:
                current_consecutive_losses += 1
                if current_consecutive_losses > max_consecutive_losses:
                    max_consecutive_losses = current_consecutive_losses
            else:
                current_consecutive_losses = 0
        
        print(f"最大连续亏损次数: {max_consecutive_losses}")
        
        # 检查是否有连续超过5次的亏损
        if max_consecutive_losses >= 5:
            print("⚠️ 警告: 检测到连续亏损超过5次!")
            return False
        else:
            print("✅ 连续亏损在可控范围内")
            return True
            
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(__file__), "data", "data.db")
    
    if os.path.exists(db_path):
        print(f"检查数据库: {db_path}")
        get_consecutive_losses(db_path)
    else:
        print(f"数据库文件未找到: {db_path}")
