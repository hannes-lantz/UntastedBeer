import csv
import os
from playwright.sync_api import sync_playwright

script_dir = os.path.dirname(os.path.abspath(__file__))

country_ids = {
    "australien": 28,
    "österrike": 29,
    "belgien": 30,
    "kanada": 32,
    "folkrepubliken kina": 33,
    "kroatien": 35,
    "tjeckien": 37,
    "danmark": 38,
    "storbritannien": 41,
    "estland": 42,
    "finland": 43,
    "frankrike": 44,
    "tyskland": 46,
    "grekland": 47,
    "irland": 52,
    "italien": 54,
    "japan": 56,
    "litauen": 60,
    "mexiko": 63,
}


def systemet(country_name):
    with sync_playwright() as p:
        browser =  p.chromium.launch(headless=True)
        page =  browser.new_page()
        page.goto(f'https://www.systembolaget.se/sortiment/ol/{country_name}/')

        # Handling age prompt
        age_buttons =  page.query_selector_all('.css-c6bmr8.e3whs8q0 a.e180zcpo2.css-1bzli92.ev9wvac0')
        if len(age_buttons) >= 2:
             age_buttons[1].click()  # Click the over 20 link

        # Handling cookie prompt
        cookie_button =  page.query_selector('button.css-ybx98v.ev9wvac0')
        if cookie_button:
             cookie_button.click()

        # Wait for the dynamic elements to load
        page.wait_for_load_state('domcontentloaded')

        # Wait for the specific <p> elements to exist
        page.wait_for_selector('p.css-18wuxp4.e3wog7r0', state="attached")

        # Find and save all matching <p> elements to a list
        p_elements =  page.query_selector_all('p.css-54mqg2.e3wog7r0')
        beer_names = [ p_element.text_content() for p_element in p_elements]

        browser.close()
        return beer_names

def get_untappd_data(username, country_id):
    with sync_playwright() as p:
        browser =  p.chromium.launch(headless=True)
        page =  browser.new_page()
        page.goto(f'https://untappd.com/user/{username}/beers?country_id={country_id}&sort=date')

        # Wait for the content to load
        page.wait_for_selector('.beer-item')

        # Accept cookies if the consent button exists
        consent_button =  page.query_selector('.fc-button.fc-cta-consent.fc-primary-button')
        if consent_button:
             consent_button.click()

        # Wait for the content to load after accepting cookies
        page.wait_for_selector('.distinct-list-list')

        # Find and process each beer item
        beer_items =  page.query_selector_all('.distinct-list-list .beer-item')
        beer_info_list = []

        for beer_item in beer_items:
            beer_name =  beer_item.query_selector('.name a.track-click').text_content()
            brewery_name =  beer_item.query_selector('.brewery a.track-click').text_content()
            style =  beer_item.query_selector('.style').text_content()

            beer_info_list.append({
                "Beer Name": beer_name,
                "Brewery Name": brewery_name,
                "Style": style
            })

        browser.close()
        return beer_info_list


def print_beer_list(beer_list, title):
    print("=" * 50)
    print(title)
    print("=" * 50)
    for idx, item in enumerate(beer_list, start=1):
        print(f"Beer {idx}: {item}")
    print("-" * 50)

def print_unique_systemet_beers(systemet_beer_names, untappd_beer_info):
    unique_systemet_beers = [
        beer for beer in systemet_beer_names if not any(
            untappd_name["Beer Name"] in beer for untappd_name in untappd_beer_info
        )
    ]

    if unique_systemet_beers:
        print("=" * 50)
        print("Unique Systemet Beers")
        print("=" * 50)
        for idx, beer in enumerate(unique_systemet_beers, start=1):
            print(f"Beer {idx}: {beer}")
        print("-" * 50)
    else:
        print("No unique Systemet beers found.")


def read_existing_csv(country_name):
    filename = os.path.join(script_dir, f"{country_name}_untappd_beers.csv")
    existing_data = []
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_data.append({
                    "Beer Name": row["Beer Name"],
                    "Brewery Name": row["Brewery Name"],
                    "Style": row["Style"],
                })
    except FileNotFoundError:
        pass
    return existing_data

def update_csv_with_new_data(beer_info_list, country_name):
    filename = os.path.join(script_dir, f"{country_name}_untappd_beers.csv")
    existing_data = read_existing_csv(country_name)

    for beer_info in beer_info_list:
        if beer_info not in existing_data:
            existing_data.append(beer_info)

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Beer Name", "Brewery Name", "Style"])
        for beer_info in existing_data:
            writer.writerow([beer_info["Beer Name"], beer_info["Brewery Name"], beer_info["Style"]])

    print(f"Beer info saved and updated in {filename}")


def main():
    username = input("Enter your Untappd username: ")
    country_name = input("Enter a country name: ")

    if country_name not in country_ids:
        print(f"Country '{country_name}' not found in the dictionary.")
    else:
        country_id = country_ids.get(country_name)
        systemet_beer_names = systemet(country_name)
        existing_data = read_existing_csv(country_name)
        untappd_beer_info = get_untappd_data(username, country_id)
        
        combined_data = set(tuple(item.items()) for item in existing_data)
        combined_data.update(tuple(item.items()) for item in untappd_beer_info)
        untappd_beer_info = [dict(item) for item in combined_data]  
        
        update_csv_with_new_data(untappd_beer_info, country_name)
        

        while True:
            print("\nChoose an option:")
            print("1. Print Systemet Beer Names")
            print("2. Print Untappd Beer Info")
            print("3. Print Not tasted Systemet Beers")
            print("4. Input Another Country")
            print("5. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                print_beer_list(systemet_beer_names, "Systemet Beer Names")
            elif choice == '2':
                print_beer_list(untappd_beer_info, "Untappd Beer Info")
            elif choice == '3':
                print_unique_systemet_beers(systemet_beer_names, untappd_beer_info)
            elif choice == '4':
                country_name = input("Enter a country name: ")
                country_id = country_ids.get(country_name)
                systemet_beer_names = systemet(country_name)
                untappd_beer_info = get_untappd_data(username, country_id)
                continue
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please enter a valid option.")


if __name__ == '__main__':
    main()




