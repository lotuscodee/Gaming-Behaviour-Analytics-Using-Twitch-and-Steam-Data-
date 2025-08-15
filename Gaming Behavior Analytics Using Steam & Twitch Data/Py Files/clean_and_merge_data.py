import pandas as pd

def clean_and_merge_data():
    """
    Loads, cleans, and merges the Steam and Twitch datasets.
    """
    print("Starting the data cleaning and merging process...")

    try:
        steam_df = pd.read_csv('steam_all_games.csv')
        twitch_df = pd.read_csv('twitch_top_100_games.csv')
        print("Successfully loaded 'steam_all_games.csv' and 'twitch_top_100_games.csv'.")
    except FileNotFoundError as e:
        print(f"Error: Make sure your CSV files are in the same folder as the script. {e}")
        return

    print("\nCleaning the Steam dataset...")
  
    steam_df.dropna(subset=['name'], inplace=True)
    
    steam_df.drop_duplicates(subset=['appid'], inplace=True)
    
    steam_df['name_standardized'] = steam_df['name'].str.lower()
    print(f"Steam data cleaned. Shape after cleaning: {steam_df.shape}")


    print("\nCleaning the Twitch dataset...")
   
    twitch_df['name_standardized'] = twitch_df['name'].str.lower()
    print(f"Twitch data cleaned. Shape: {twitch_df.shape}")


    print("\nMerging the two datasets on the standardized game name...")
   
    merged_df = pd.merge(twitch_df, steam_df, on='name_standardized', how='inner')

    merged_df.rename(columns={'name_x': 'twitch_game_name', 'name_y': 'steam_game_name', 'id': 'twitch_game_id'}, inplace=True)
    
    final_df = merged_df[['twitch_game_id', 'twitch_game_name', 'appid', 'steam_game_name']]
    
    print(f"\nMerge complete! Found {len(final_df)} matching games.")
    print("Here is a preview of the final merged data:")
    print(final_df.head())

    final_df.to_csv(output_filename, index=False)
    
    print(f"\nSuccess! Cleaned and merged data saved to '{output_filename}'.")


if __name__ == "__main__":
    clean_and_merge_data()