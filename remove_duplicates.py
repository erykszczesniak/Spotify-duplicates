import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = ''
client_secret = ''
redirect_uri = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope='playlist-modify-public'))


def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


def find_duplicates(tracks):
    track_dict = {}
    duplicates = []
    for item in tracks:
        track = item['track']
        track_id = track['id']
        if track_id in track_dict:
            duplicates.append(item)
        else:
            track_dict[track_id] = track
    return duplicates


def search_track(tracks, search_query):
    found_tracks = []
    for item in tracks:
        track = item['track']
        if search_query.lower() in track['name'].lower():
            found_tracks.append(track)
    return found_tracks


def print_all_tracks(tracks):
    for i, item in enumerate(tracks):
        track = item['track']
        print(f"{i + 1}. {track['name']} by {track['artists'][0]['name']}")


def remove_specific_duplicates(playlist_id, duplicates, indices):
    track_uris = [duplicates[i]['track']['uri'] for i in indices]
    sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)


def remove_all_duplicates(playlist_id, duplicates):
    track_uris = [item['track']['uri'] for item in duplicates]
    sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)


def main():
    # Get the user's playlists
    playlists = sp.current_user_playlists()
    print("Select a playlist to manage:")
    for i, playlist in enumerate(playlists['items']):
        print(f"{i + 1}. {playlist['name']}")
    choice = int(input("Enter the number of the playlist: ")) - 1
    playlist_id = playlists['items'][choice]['id']

    # Get tracks in the selected playlist
    tracks = get_playlist_tracks(playlist_id)

    while True:
        print("\nOptions:")
        print("1. Find duplicates")
        print("2. Search for a track")
        print("3. Print all tracks")
        print("4. Exit")
        option = int(input("Choose an option: "))

        if option == 1:
            duplicates = find_duplicates(tracks)
            if not duplicates:
                print("No duplicates found.")
            else:
                print("Duplicates found:")
                for i, item in enumerate(duplicates):
                    track = item['track']
                    print(f"{i + 1}. {track['name']} by {track['artists'][0]['name']}")

                # Ask to remove duplicates
                remove = input(
                    "Do you want to remove duplicates? Enter 'all' to remove all duplicates, or specify the numbers of "
                    "the duplicates you want to remove, separated by commas: ").strip().lower()
                if remove == 'all':
                    remove_all_duplicates(playlist_id, duplicates)
                    print("All duplicates removed.")
                elif remove:
                    indices = [int(index.strip()) - 1 for index in remove.split(',')]
                    remove_specific_duplicates(playlist_id, duplicates, indices)
                    print("Selected duplicates removed.")
                else:
                    print("No duplicates were removed.")

        elif option == 2:
            search_query = input("Enter the track name to search for: ")
            found_tracks = search_track(tracks, search_query)
            if found_tracks:
                print(f"Tracks matching '{search_query}':")
                for i, track in enumerate(found_tracks):
                    print(f"{i + 1}. {track['name']} by {track['artists'][0]['name']}")
            else:
                print(f"No tracks found matching '{search_query}'.")

        elif option == 3:
            print_all_tracks(tracks)

        elif option == 4:
            print("Exiting...")
            break

        else:
            print("Invalid option. Please choose again.")


if __name__ == '__main__':
    main()
