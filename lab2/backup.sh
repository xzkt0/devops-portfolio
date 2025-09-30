#!/usr/bin/env bash
set -euo pipefail

# === Config ===
SRC_DIR="${1:-}"                         
BACKUP_DIR="/mnt/c/Users/Admin/Desktop/Chnu/Chnu/devops/lab2/backup"
LOG_DIR="${LOG_DIR:-$HOME/backup-logs}"  
RETENTION="${RETENTION:-5}"              

# Твій Discord Webhook
DISCORD_WEBHOOK="https://discord.com/api/webhooks/1420016129673400453/1qrUQp9It-poP1PxwGs16hwNxCnWvHoB_c5sbtE7GfOfzOvezQJttmR1A3La795u4nLV"

mkdir -p "$BACKUP_DIR" "$LOG_DIR"
ts="$(date +'%Y-%m-%d_%H-%M-%S')"
archive="${BACKUP_DIR}/backup_${ts}.tar.gz"
logfile="${LOG_DIR}/backup_${ts}.log"

if [[ -z "${SRC_DIR}" || ! -d "${SRC_DIR}" ]]; then
  echo "Usage: $0 <folder_to_backup>"
  exit 1
fi

{
  echo "[$(date)] Starting backup of: ${SRC_DIR}"
  echo "Target archive: ${archive}"

  tar -czf "${archive}" -C "$(dirname "${SRC_DIR}")" "$(basename "${SRC_DIR}")"
  echo "[$(date)] Done, size: $(du -h "${archive}" | awk '{print $1}')"

  echo "[$(date)] Pruning old backups, keeping last ${RETENTION}"
  ls -1t "${BACKUP_DIR}"/backup_*.tar.gz 2>/dev/null | tail -n +$((RETENTION+1)) | xargs -r rm -f
  echo "[$(date)] Prune complete"

} | tee -a "${logfile}"

# Повідомлення в Discord
msg="✅ Backup completed: $(basename "${archive}")"
curl -s -H "Content-Type: application/json" \
  -X POST -d "{\"content\":\"${msg}\"}" "${DISCORD_WEBHOOK}" >/dev/null || true
