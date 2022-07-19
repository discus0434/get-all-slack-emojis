"""Get all custom emojis in your workspace."""
import os
import argparse
from typing import Any, Dict, Union
from http.client import IncompleteRead
import urllib.error
import urllib.request

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def get_custom_emoji_dict(client: Any) -> Union[Dict[str, str], None]:
    """Get a dictionary of emoji's name & url pair

    Args:
        client (Any): A web client allows apps to communicate with
            the Slack Platform's Web API.

    Returns:
        Union[Dict[str, str], None]: Dict contains image-url and name of
            all custom emojis in your workspace.
    """
    # Try to communicate with Slack API {RETRY} times.
    RETRY = 3

    for _ in range(RETRY):
        try:
            res = client.emoji_list()
        except SlackApiError as e:
            print("Error: ", e.response["error"])
        except IncompleteRead as e:
            print("IncompleteRead Exception: ", e)
        except ConnectionError as e:
            print("ConnectionError: ", e)
        else:
            break
    # If all trials fail, return None
    else:
        print("Failed to get custom emoji_path list.")
        return None

    # If some trial ends successfully, make emoji dict from response
    # Exclude aliases
    emoji_dict = remove_aliases(emoji_dict=res["emoji"])

    return emoji_dict


def remove_aliases(emoji_dict: Dict[str, str]) -> Dict[str, str]:
    """Remove aliases of emojis's name from dict

    In response of client.emoji_list(), alias has a real name as a value
    while a real one has image-url. Since it causes inconvenience to
    leave it as it is, just remove.

    Args:
        emoji_dict (Dict[str, str]): Dict includes some alias of emoji.

    Returns:
        Dict[str, str]: Dict contains image-url and name of
            all custom emojis in your workspace.
    """
    emoji_dict = {
        name: url for name, url in emoji_dict.items() if not url.startswith("alias:")
    }
    return emoji_dict


def download_file(url: str, path: str) -> None:
    """Download a image from an appointed url to an appointed path.

    Args:
        url (str): url to image file
        path (str): path to save image
    """
    try:
        with urllib.request.urlopen(url) as url, open(path, "wb") as path:
            path.write(url.read())
    # if an appointed url is invalid, just print the error, not raise
    except urllib.error.URLError as e:
        print(e)

    return None


def download_file_from_dict(dict: Dict[str, str], dist_dir: str) -> None:
    """Download all images written in a dict contains name & url pair

    Downloaded images are named according to a name paired
    with its image-url.

    Args:
        dict (Dict[str, str]): emoji dict
        dist_dir (str): output directory
    """
    os.makedirs(dist_dir, exist_ok=True)
    for name, url in dict.items():
        ext = url.split(".")[-1]
        path = os.path.join(dist_dir, name + "." + ext)
        download_file(url=url, path=path)

    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="Oauth token for slack api.")
    parser.add_argument(
        "-o", "--output", help="output location of images", default=os.getcwd()
    )
    args = parser.parse_args()

    client = WebClient(token=args.token)
    emoji_dict = get_custom_emoji_dict(client=client)

    download_file_from_dict(dict=emoji_dict, dist_dir=args.output)

    return None


if __name__ == "__main__":
    main()
