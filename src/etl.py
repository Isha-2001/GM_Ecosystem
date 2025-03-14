import requests
import pandas as pd
import time

# Companies House API key (replace with your actual key)
API_KEY = "8b05f2e5-fe2d-492c-a258-b6037ca9a6ec"
BASE_URL = "https://api.company-information.service.gov.uk"

SIC_CODES = "62012,62090,63110,7371,7372,7379,7382"

def search_companies(sic_code, start_index=0):
    companies = []
    batch_size = 100  # API returns up to 100 results per request
    url = f"{BASE_URL}/advanced-search/companies"
    params = {
        "sic_codes": sic_code,
        "location": "Manchester",
        "start_index": start_index,
    }
    
    try:
        response = requests.get(url, auth=(API_KEY, ""), params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data["items"]:
                companies.append({
                    "Company Name": item.get("company_name", "N/A"),
                    "Company Number": item.get("company_number", "N/A"),
                    "Company Status": item.get("company_status", "N/A"),
                    "Company Type": item.get("company_type", "N/A"),
                    "Date of Creation": item.get("date_of_creation", "N/A"),
                    "Date of Cessation": item.get("date_of_cessation", "N/A"),
                    "Registered Office Address": item.get("registered_office_address", {}).get("address_line_1", "N/A"),
                    "Locality": item.get("registered_office_address", {}).get("locality", "N/A"),
                    "Postal Code": item.get("registered_office_address", {}).get("postal_code", "N/A"),
                    "Region": item.get("registered_office_address", {}).get("region", "N/A"),
                    "SIC Codes": ', '.join(item.get("sic_codes", [])),
                })
            # Pagination
            start_index += batch_size
            time.sleep(1)  # Avoid hitting rate limits
        else:
            print(f"⚠️ Error {response.status_code}: {response.text}")
    
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        time.sleep(5)  # Wait & retry

    return companies

def fetch_companies(sic_codes):
    companies = []
    start_index = 0
    while True:
        new_companies = search_companies(sic_codes, start_index)
        if not new_companies:
            break
        companies.extend(new_companies)
        start_index += 100  # Move to the next batch
    return pd.DataFrame(companies)

def main():
    df = fetch_companies(SIC_CODES)
    if not df.empty:
        df.to_csv("data/companies_ai_cybersecurity_raw.csv", index=False)
        print(f"✅ Data saved to companies_ai_cybersecurity_raw.csv ({len(df)} companies)")
    else:
        print("⚠️ No company data fetched.")

if __name__ == "__main__":
    main()
