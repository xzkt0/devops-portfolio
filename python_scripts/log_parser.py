#!/usr/bin/env python3
import re
import argparse
from collections import Counter
from datetime import datetime

parser = argparse.ArgumentParser(description="Parse Apache/Nginx logs and generate HTML report.")
parser.add_argument("--input", required=True, help="Path to access.log file")
parser.add_argument("--output", default="report.html", help="Output HTML report")
args = parser.parse_args()


with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
    logs = f.readlines()

ip_pattern = r'(\d+\.\d+\.\d+\.\d+)'
user_agent_pattern = r'"[^"]*"$'
status_pattern = r'"\s(\d{3})\s'

ips, agents, statuses = [], [], []

for line in logs:
    if match := re.search(ip_pattern, line):
        ips.append(match.group(1))
    if match := re.search(user_agent_pattern, line):
        agents.append(match.group(0).strip('"'))
    if match := re.search(status_pattern, line):
        statuses.append(match.group(1))

# === Підрахунок ===
top_ips = Counter(ips).most_common(5)
top_agents = Counter(agents).most_common(5)
top_status = Counter(statuses).most_common()

# === Генерація HTML ===
html = f"""
<html>
<head>
<title>Web Log Report</title>
<style>
body {{ font-family: Arial; background-color: #f5f5f5; }}
h1 {{ color: #333; }}
table {{ border-collapse: collapse; width: 60%; margin-bottom: 30px; }}
th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
th {{ background-color: #ddd; }}
</style>
</head>
<body>
<h1>Web Log Analysis Report</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

<h2>Top 5 IP Addresses</h2>
<table><tr><th>IP</th><th>Requests</th></tr>
{''.join([f"<tr><td>{ip}</td><td>{count}</td></tr>" for ip, count in top_ips])}
</table>

<h2>Top 5 User Agents</h2>
<table><tr><th>User Agent</th><th>Count</th></tr>
{''.join([f"<tr><td>{ua}</td><td>{count}</td></tr>" for ua, count in top_agents])}
</table>

<h2>HTTP Status Codes</h2>
<table><tr><th>Status</th><th>Count</th></tr>
{''.join([f"<tr><td>{code}</td><td>{count}</td></tr>" for code, count in top_status])}
</table>
</body></html>
"""

with open(args.output, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Report saved to {args.output}")

