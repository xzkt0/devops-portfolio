#!/usr/bin/env python3
import requests
import time
import csv
import json
from datetime import datetime

# === Discord Webhook ===
WEBHOOK_URL = "https://discord.com/api/webhooks/1420016129673400453/1qrUQp9It-poP1PxwGs16hwNxCnWvHoB_c5sbtE7GfOfzOvezQJttmR1A3La795u4nLV"

# === Ендпоінти для тесту ===
ENDPOINTS = [
    "https://google.com",            # робочий
    "https://thiswebsitedoesnotexist12345.com",  # з помилкою
    "https://github.com"             # робочий
]

CSV_FILE = "api_monitor.csv"
JSON_FILE = "api_monitor.json"

def send_alert(message):
    """Відправка алерту в Discord"""
    payload = {"content": f":rotating_light: {message}"}
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"⚠️ Не вдалося відправити повідомлення в Discord: {e}")

def check_endpoint(url):
    """Перевірка доступності ендпоінта"""
    start = time.time()
    try:
        response = requests.get(url, timeout=4)
        elapsed = round(time.time() - start, 3)
        status = response.status_code
        print(f"✅ {url} — {status} ({elapsed}s)")
        return {"url": url, "status": status, "response_time": elapsed, "timestamp": datetime.now().isoformat()}
    except requests.RequestException as e:
        elapsed = round(time.time() - start, 3)
        print(f"❌ {url} — FAILED ({elapsed}s)")
        send_alert(f"Endpoint `{url}` failed after {elapsed}s! Error: {e}")
        return {"url": url, "status": "FAIL", "response_time": elapsed, "timestamp": datetime.now().isoformat()}

# === Основна логіка ===
results = [check_endpoint(url) for url in ENDPOINTS]

# === Збереження у CSV ===
with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

# === Збереження у JSON ===
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)

print(f"\n📄 Результати збережено у {CSV_FILE} та {JSON_FILE}")
print("✅ Якщо все працює, сповіщення про помилку вже має бути у Discord!")
