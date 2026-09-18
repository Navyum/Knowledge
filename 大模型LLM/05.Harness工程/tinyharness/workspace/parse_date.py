"""贯穿全课的示例任务目标文件。

现状：parse_date 只处理不带时区的 ISO 字符串。
任务：给它补上带时区偏移（如 2024-01-01T12:00:00+08:00）的支持，并让单测通过。
"""
from datetime import datetime, timezone, timedelta


def parse_date(s: str) -> datetime:
    """解析 ISO 8601 日期字符串。

    支持：
      - 纯日期 / 日期时间（无时区）
      - 带时区偏移 +HH:MM / -HH:MM
      - 结尾 Z（UTC）
    """
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)
