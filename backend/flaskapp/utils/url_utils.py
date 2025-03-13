class UrlUtils:

    @staticmethod
    def encode_url(url: str):
        """
        Encode the given url with percentage, i.e http://Hello/World -> http%3A%2F%2FHello%2FWorld
        :param url: url The url string to encode.
        :return: The encoded url string.
        """
        url = url.replace(":", "%3A")
        url = url.replace("/", "%2F")
        return url
