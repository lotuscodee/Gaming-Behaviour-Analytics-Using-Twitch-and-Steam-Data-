import requests
import pandas as pd

CLIENT_SECRET = '8fow3n5f1ys0kxpf80v3dcleexnst3'

def get_twitch_access_token(client_id, client_secret):
    """
    Sends your credentials to Twitch to get an access token.
    """
    print("Requesting Access Token from Twitch...")

    auth_url = 'https://id.twitch.tv/oauth2/token'

    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }

    try:
     
        response = requests.post(auth_url, params=params)
   
        if response.status_code == 200:
            data = response.json()
            access_token = data['access_token']
            print("Access Token received successfully!")
            return access_token
        else:
            print(f"Error getting token: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        return None

def get_top_games(client_id, access_token):
    """
    Fetches the top 100 most-watched games from Twitch using the access token.
    """
    if not access_token:
        print("Cannot fetch games without a valid Access Token.")
        return None
        
    print("\nFetching top games from Twitch...")
    
    games_url = 'https://api.twitch.tv/helix/games/top'

    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}' 
    }
  
    params = {
        'first': 100 
    }

    try:
        response = requests.get(games_url, headers=headers, params=params)
        
        if response.status_code == 200:
            print("Successfully fetched top games data!")
            data = response.json()
       
            top_games_list = data['data']
          
            df = pd.DataFrame(top_games_list)
            
            print("Here is a preview of the data:")
            print(df.head())
        
            output_filename = 'twitch_top_100_games.csv'
            df.to_csv(output_filename, index=False)
            
            print(f"\nSuccess! Top games data saved to '{output_filename}'")
            return df

        else:
            print(f"Error fetching games: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"An error occurred while fetching games: {e}")
        return None


if __name__ == "__main__":

    token = get_twitch_access_token(CLIENT_ID, CLIENT_SECRET)

    if token:
        get_top_games(CLIENT_ID, token)