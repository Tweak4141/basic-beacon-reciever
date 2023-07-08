class Cache:
    def __init__(self):
        self.cache = {}

    def getKey(self, key: str) -> any:
        """
        Gets a key from the cache
        :param key: str
        :return: any
        """
        return self.cache.get(key)

    def setKey(self, key: str, value: any) -> None:
        """
        Sets a key in the cache
        :param key: str
        :param value: any
        :return: None
        """
        self.cache.update({key: value})

    def deleteKey(self, key: str) -> None:
        """
        Deletes a key from the cache
        :param key: str
        :return: None
        """
        self.cache.pop(key)
    
    def clearCache(self) -> None:
        """
        Clears the cache
        :return: None
        """
        self.cache = {}

    def deleteMultipleKeys(self, keys: list) -> None:
        """
        Deletes multiple keys from the cache
        :param keys: list
        :return: None
        """
        for key in keys:
            self.cache.pop(key)
