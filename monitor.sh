#!/bin/bash

# ===== Налаштування =====
WEBHOOK_URL="https://discord.com/api/webhooks/1420016129673400453/1qrUQp9It-poP1PxwGs16hwNxCnWvHoB_c5sbtE7GfOfzOvezQJttmR1A3La795u4nLV"
LOG_FILE="./monitor.log"

CPU_THRESHOLD=80
RAM_THRESHOLD=80
DISK_THRESHOLD=90

# ===== Функції =====
send_alert() {
    local message="$1"
    curl -H "Content-Type: application/json" \
         -X POST \
         -d "{\"content\":\":rotating_light: $message\"}" \
         "$WEBHOOK_URL"
    echo "$(date '+%Y-%m-%d %H:%M:%S') ALERT: $message" >> "$LOG_FILE"
}

# ===== CPU =====
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}')
CPU_INT=${CPU_USAGE%.*}

if [ "$CPU_INT" -gt "$CPU_THRESHOLD" ]; then
    send_alert "CPU usage is at ${CPU_INT}% (> ${CPU_THRESHOLD}%)"
fi

# ===== RAM =====
RAM_USAGE=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
RAM_INT=${RAM_USAGE%.*}

if [ "$RAM_INT" -gt "$RAM_THRESHOLD" ]; then
    send_alert "RAM usage is at ${RAM_INT}% (> ${RAM_THRESHOLD}%)"
fi

# ===== DISK =====
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt "$DISK_THRESHOLD" ]; then
    send_alert "Disk usage is at ${DISK_USAGE}% (> ${DISK_THRESHOLD}%)"
fi
