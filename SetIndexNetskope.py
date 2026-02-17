"""
Reset Netskope Iterator Index (netskope-foundry-daily) for Malsite & Malware Alerts
Sets the index to the current epoch time.

Usage:
    python reset_index.py <tenant_fqdn> <api_token>

Example:
    python reset_index.py myorg.goskope.com xxxxxxxxxxxxxxxx
"""

import sys
import time
import requests
from datetime import datetime, timezone

ALERT_TYPES = ["malsite", "malware"]
INDEX_NAME = "netskope-foundry-daily"

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <tenant_fqdn> <api_token>")
        sys.exit(1)

    tenant = sys.argv[1].strip().rstrip("/")
    token = sys.argv[2].strip()
    base_url = f"https://{tenant}" if not tenant.startswith("https://") else tenant
    epoch = int(time.time())

    print(f"Tenant    : {base_url}")
    print(f"Index     : {INDEX_NAME}")
    print(f"Operation : {epoch} ({datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat()})")
    print("-" * 50)

    for alert_type in ALERT_TYPES:
        url = f"{base_url}/api/v2/events/dataexport/alerts/{alert_type}"
        headers = {"Netskope-Api-Token": token}
        params = {"index": INDEX_NAME, "operation": epoch}

        try:
            resp = requests.get(url, headers=headers, params=params, timeout=30)
            resp.raise_for_status()
            print(f"[{alert_type.upper()}] ✅ Index reset to {epoch} — {resp.json()}")
        except Exception as e:
            print(f"[{alert_type.upper()}] ❌ Failed — {e}")

if __name__ == "__main__":
    main()
