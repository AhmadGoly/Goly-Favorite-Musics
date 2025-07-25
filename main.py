import click
import json
from dotenv import load_dotenv, set_key, dotenv_values
from fetcher.new_song_tracker import NewSongTracker
from fetcher.artist_config import ArtistConfig
import os

ENV_PATH = ".env"
load_dotenv(ENV_PATH)

def _load_artists():
    raw = dotenv_values(ENV_PATH).get("ARTISTS", "{}")
    return json.loads(raw)

def _save_artists(artists):
    set_key(ENV_PATH, "ARTISTS", json.dumps(artists, ensure_ascii=False))

@click.group()
def cli():
    pass

@cli.command()
@click.option("--group", default=None, help="Artist group like 'pop' or individual artist name")
@click.option("--limit", default=10, help="Max songs per artist")
def track(group, limit):
    tracker = NewSongTracker()
    new_songs = tracker.find_new_songs(category_or_artist=group, limit_per_artist=limit)
    if new_songs.empty:
        click.echo("No new songs found.")
    else:
        click.echo(new_songs.to_string(index=False))

@cli.command()
@click.argument("group")
@click.argument("artist")
def add(group, artist):
    artists = _load_artists()
    if group not in artists:
        artists[group] = []
    if artist not in artists[group]:
        artists[group].append(artist)
        _save_artists(artists)
        click.echo(f"Added {artist} to group {group}")
    else:
        click.echo(f"{artist} already in group {group}")

@cli.command()
@click.argument("group")
@click.argument("artist")
def remove(group, artist):
    artists = _load_artists()
    if group in artists and artist in artists[group]:
        artists[group].remove(artist)
        _save_artists(artists)
        click.echo(f"Removed {artist} from group {group}")
    else:
        click.echo(f"{artist} not found in group {group}")

@cli.command()
def show():
    artists = _load_artists()
    for group, names in artists.items():
        click.echo(f"{group}: {', '.join(names)}")

if __name__ == "__main__":
    cli()
