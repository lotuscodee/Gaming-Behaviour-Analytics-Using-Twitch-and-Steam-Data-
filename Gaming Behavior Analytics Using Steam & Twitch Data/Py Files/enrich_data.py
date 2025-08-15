import pandas as pd
import requests
import time 

CLIENT_ID = 'fjqkoln2aa2ipuan97er5xytn7kmvh'
CLIENT_SECRET = '8fow3n5f1ys0kxpf80v3dcleexnst3'

def get_twitch_access_token(client_id, client_secret):
    """Gets an access token from Twitch."""
    auth_url = 'https://id.twitch.tv/oauth2/token'
    params = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'}
    try:
        response = requests.post(auth_url, params=params)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            print(f"Failed to get Twitch token: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error getting Twitch token: {e}")
        return None

def enrich_data():
    """
    Enriches the merged data with live Twitch viewers and Steam genre information.
    """
    print("Starting data enrichment process...")
 
    try:
        df = pd.read_csv('final_merged_games.csv')
    except FileNotFoundError:
        print("Error: 'final_merged_games.csv' not found. Please run the clean_and_merge script first.")
        return

    print("Fetching live viewer counts from Twitch...")
    access_token = get_twitch_access_token(CLIENT_ID, CLIENT_SECRET)
    if not access_token:
        return

    headers = {'Client-ID': CLIENT_ID, 'Authorization': f'Bearer {access_token}'}
    
    game_ids = df['twitch_game_id'].tolist()
    streams_url = 'https://api.twitch.tv/helix/streams'
    
    all_stream_data = []
    for i in range(0, len(game_ids), 100):
        chunk = game_ids[i:i+100]
        params = {'game_id': chunk, 'first': 100}
        response = requests.get(streams_url, headers=headers, params=params)
        if response.status_code == 200:
            all_stream_data.extend(response.json()['data'])
        else:
            print(f"Failed to fetch stream data: {response.status_code}")
        time.sleep(1)
   
    viewer_counts = {}
    for stream in all_stream_data:
        game_id = stream['game_id']
        viewer_count = stream['viewer_count']
        if game_id in viewer_counts:
            viewer_counts[game_id] += viewer_count
        else:
            viewer_counts[game_id] = viewer_count
  
    df['viewer_count'] = df['twitch_game_id'].map(viewer_counts).fillna(0).astype(int)

    print("Fetching genre information from Steam...")
    genres_list = []
    for appid in df['appid']:
  
        steam_url = f"http://store.steampowered.com/api/appdetails?appids={appid}"
        try:
            response = requests.get(steam_url)
            if response.status_code == 200:
                data = response.json()
                if str(appid) in data and data[str(appid)]['success']:
                    genres = data[str(appid)]['data'].get('genres', [])
                    primary_genre = genres[0]['description'] if genres else 'N/A'
                    genres_list.append(primary_genre)
                else:
                    genres_list.append('N/A')
            else:
                genres_list.append('N/A')
        except Exception:
            genres_list.append('N/A')
        
        time.sleep(0.5) 

    df['genre'] = genres_list
    
    print("\nEnrichment complete! Here is a preview of the new data:")
    print(df.head())
  
    output_filename = 'enriched_gaming_data.csv'
    df.to_csv(output_filename, index=False)
    print(f"\nSuccess! Enriched data saved to '{output_filename}'.")

if __name__ == "__main__":
    enrich_data()