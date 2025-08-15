import requests
import pandas as pd 
import json 

def get_all_steam_games():
    """
    Fetches the complete list of all games on Steam and saves them to a CSV file.
    """
    print("Starting the data collection process...")

    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

    try:
       
        response = requests.get(url)

        if response.status_code == 200:
            print("Successfully connected to the Steam API!")

            data = response.json()

            game_list = data['applist']['apps']
            print(f"Found {len(game_list)} applications on Steam.")

            df = pd.DataFrame(game_list)
           
            print("Here is a preview of the data:")
            print(df.head())

            output_filename = 'steam_all_games.csv'
            df.to_csv(output_filename, index=False)

            print(f"\nSuccess! All game data has been saved to '{output_filename}'")

        else:
            print(f"Error: Failed to fetch data. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_all_steam_games()