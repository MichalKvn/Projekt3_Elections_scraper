"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Michal Kavan
email: kavan1@centrum.cz
discord: Michal K.#5207
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

LINE = 30 * "-"

def check_arguments():
    if len(sys.argv) != 3:
        print("You typed the wrong number of arguments")
        sys.exit(1)

def parse_arguments():
    web_link = sys.argv[1]
    cvs_file = sys.argv[2]
    return web_link, cvs_file

def verify_link_format(link):
    if link.startswith("https://volby.cz/pls/ps2017nss"):
        pass
    else:
        print("Incorrect arguments order or format")
        sys.exit(1)

def verify_net_link(web_link):
    try:
        response = requests.get(web_link)
        response.raise_for_status()

        if response.status_code == 200:
            pass
        else:
            print(f"Invalid response status code: {response.status_code}")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("You typed an invalid link or there was an issue with the request")
        sys.exit(1)

def get_city_numbers(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    city_numbers = []
    
    city_number_cells = soup.find_all("td", class_="cislo", headers=["t1sa1 t1sb1", "t2sa1 t2sb1", "t3sa1 t3sb1"])
    
    for number_cell in city_number_cells:
        city_number = number_cell.text.strip()
        city_numbers.append(city_number)
    
    return city_numbers
    
def get_city_names(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    city_names = []
    
    city_name_cells = soup.find_all("td", class_="overflow_name", headers=["t1sa1 t1sb2","t2sa1 t2sb2","t3sa1 t3sb2" ])
    
    for city_cell in city_name_cells:
        city_name = city_cell.text.strip()
        city_names.append(city_name)
    
    return city_names

def get_voters_count(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    link_cells = soup.find_all("td", class_="cislo", headers=["t1sa1 t1sb1", "t2sa1 t2sb1", "t3sa1 t3sb1"])
    
    voters_counts = []  
    
    for cell in link_cells:
        link_element = cell.find("a", href=True)
        if link_element:
            link_url = f"https://volby.cz/pls/ps2017nss/{link_element['href']}"
            response = requests.get(link_url)
            new_soup = BeautifulSoup(response.text, 'html.parser')
            voters = new_soup.find("td", class_="cislo", headers="sa2")
            if voters is not None:
                voters_counts.append(voters.text)  
    
    return voters_counts

def get_voters_votes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    link_cells = soup.find_all("td", class_="cislo", headers=["t1sa1 t1sb1", "t2sa1 t2sb1", "t3sa1 t3sb1"])
    
    voters_votes = []
    
    for cell in link_cells:
        link_element = cell.find("a", href=True)
        if link_element:
            link_url = f"https://volby.cz/pls/ps2017nss/{link_element['href']}"
            response = requests.get(link_url)
            new_soup = BeautifulSoup(response.text, 'html.parser')
            voters = new_soup.find("td", class_="cislo", headers="sa3")
            if voters is not None:
                voters_votes.append(voters.text)  
    
    return voters_votes


def get_voters_votes_valid(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    link_cells = soup.find_all("td", class_="cislo", headers=["t1sa1 t1sb1", "t2sa1 t2sb1", "t3sa1 t3sb1"])

    voters_valid = []
    
    for cell in link_cells:
        link_element = cell.find("a", href=True)
        if link_element:
            link_url = f"https://volby.cz/pls/ps2017nss/{link_element['href']}"
            response = requests.get(link_url)
            new_soup = BeautifulSoup(response.text, 'html.parser')
            voters = new_soup.find("td", class_="cislo", headers="sa6")
            if voters is not None:
                voters_valid.append(voters.text) 
    
    return voters_valid

def get_parties_and_votes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    link_cells = soup.find_all("td", class_="cislo", headers=["t1sa1 t1sb1", "t2sa1 t2sb1", "t3sa1 t3sb1"])

    parties_and_votes = {}

    for cell in link_cells:
        link_element = cell.find("a", href=True)
        if link_element:
            link_url = f"https://volby.cz/pls/ps2017nss/{link_element['href']}"
            response = requests.get(link_url)
            new_soup = BeautifulSoup(response.text, 'html.parser')
            
            party_name_cells = new_soup.find_all("td", class_="overflow_name", headers=["t1sa1 t1sb2", "t2sa1 t2sb2"])
            voters_cells = new_soup.find_all("td", class_="cislo", headers=["t1sa2 t1sb3", "t2sa2 t2sb3"])
            
            for party_name_cell, voters_cell in zip(party_name_cells, voters_cells):
                party_name = party_name_cell.get_text().strip()
                voters = voters_cell.get_text().strip()
                if party_name in parties_and_votes:
                    parties_and_votes[party_name].append(voters)
                else:
                    parties_and_votes[party_name] = [voters]

    return parties_and_votes

def create_csv(city_numbers, city_names, voters_counts, voters_votes, voters_valid, parties_and_votes, cvs_file):
    with open(f"{cvs_file}.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        
        header = ['City Number', 'City Name', 'Voters Count', 'Voters Votes', 'Voters Valid'] + list(parties_and_votes.keys())
        writer.writerow(header)
        
        max_votes = max(len(votes) for votes in parties_and_votes.values())
        
        for i in range(len(city_numbers)):
            row = [city_numbers[i], city_names[i], voters_counts[i], voters_votes[i], voters_valid[i]]
            
            for party_name in parties_and_votes.keys():
                if i < len(parties_and_votes[party_name]):
                    row.append(parties_and_votes[party_name][i])
                else:
                    row.append("")
            
            writer.writerow(row)

def main():
    check_arguments()
    web_link, cvs_file = parse_arguments()
    verify_link_format(web_link)
    verify_net_link(web_link)
    
    print(f"Link: {web_link}")
    print(f"File: {cvs_file}")
    print(LINE)
    print("Creating file...please wait")
    
    
    city_numbers = get_city_numbers(web_link)
    city_names = get_city_names(web_link)
    voters_counts = get_voters_count(web_link)
    voters_votes = get_voters_votes(web_link)
    voters_valid = get_voters_votes_valid(web_link)
    parties_and_votes = get_parties_and_votes(web_link)
    
    create_csv(city_numbers, city_names, voters_counts, voters_votes, voters_valid, parties_and_votes, cvs_file)
    
if __name__ == "__main__":
    main()