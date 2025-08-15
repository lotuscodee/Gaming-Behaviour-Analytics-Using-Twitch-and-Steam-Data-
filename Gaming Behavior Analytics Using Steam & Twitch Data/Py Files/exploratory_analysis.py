import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def perform_eda():
    """
    Performs Exploratory Data Analysis on the enriched dataset and creates visualizations.
    """
    print("Starting Exploratory Data Analysis...")
    
    try:
        df = pd.read_csv('enriched_gaming_data.csv')
    except FileNotFoundError:
        print("Error: 'enriched_gaming_data.csv' not found. Please run the enrich_data script first.")
        return

    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 7))

    print("\nAnalyzing genre popularity...")
    genre_viewers = df.groupby('genre')['viewer_count'].sum().sort_values(ascending=False).head(10)
    
    print("Top 10 Genres by Viewer Count:")
    print(genre_viewers)

    ax = sns.barplot(x=genre_viewers.index, y=genre_viewers.values, palette='viridis')
    plt.title('Top 10 Most Watched Genres on Twitch', fontsize=16)
    plt.xlabel('Genre', fontsize=12)
    plt.ylabel('Total Viewer Count', fontsize=12)
    plt.xticks(rotation=45, ha='right') 
    plt.tight_layout() 
    
    plt.savefig('genre_popularity.png')
    print("Saved 'genre_popularity.png'")


    print("\nAnalyzing top individual games...")
    plt.figure(figsize=(12, 7)) 
    
    top_games = df.sort_values(by='viewer_count', ascending=False).head(10)
    
    print("\nTop 10 Games by Viewer Count:")
    print(top_games[['twitch_game_name', 'viewer_count', 'genre']])
    
    ax2 = sns.barplot(x='viewer_count', y='twitch_game_name', data=top_games, palette='plasma')
    plt.title('Top 10 Most Watched Games on Twitch', fontsize=16)
    plt.xlabel('Total Viewer Count', fontsize=12)
    plt.ylabel('Game', fontsize=12)
    plt.tight_layout()

    plt.savefig('top_games_popularity.png')
    print("Saved 'top_games_popularity.png'")
    
    print("\nEDA complete! Check the generated .png files for your visualizations.")

if __name__ == "__main__":
    perform_eda()