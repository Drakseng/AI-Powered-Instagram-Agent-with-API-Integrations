from instagrapi import Client


def login_instagram(username: str, password: str) -> Client:
    """
    Login to Instagram using the provided username and password.

    Returns:
        Authenticated instagrapi Client.
    """
    cl = Client()
    cl.login(username, password)
    return cl


def upload_photo(cl: Client, image_path: str, caption: str) -> None:
    """
    Upload a photo with a caption to Instagram using an authenticated instagrapi client.
    """
    cl.photo_upload(path=image_path, caption=caption)
