import requests

API_URL = "https://freeproxy24.com/api/free-proxy-list?limit=500&page=1&sortBy=lastChecked&sortType=desc"

def fetch_proxies():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def save_proxies_by_type(proxies):
    # Prepare a dict to hold lists by type
    proxy_buckets = {
        "http": [],
        "socks4": [],
        "socks5": []
    }

    for p in proxies:
        ip = p.get("ip")
        port = p.get("port")
        protocols = p.get("protocols", [])

        # For each protocol this proxy supports,
        # append it to that bucket
        for prot in protocols:
            if prot in proxy_buckets:
                proxy_buckets[prot].append(f"{ip}:{port}")

    # Write to separate files
    for prot, plist in proxy_buckets.items():
        filename = f"{prot}.txt"
        with open(filename, "w") as f:
            for entry in plist:
                f.write(entry + "\n")
        print(f"Saved {len(plist)} {prot} proxies → {filename}")

def main():
    print("Fetching proxies...")
    proxies = fetch_proxies()
    print(f"Total proxies fetched: {len(proxies)}")
    save_proxies_by_type(proxies)
    print("Done.")

if __name__ == "__main__":
    main()
