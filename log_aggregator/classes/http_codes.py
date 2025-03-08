import random

class HttpCodes:
    def __init__(self):
        """
        Initialize the HttpCodes class

        """
        self.codes = [
            100, 101, 102,
            200, 201, 202, 203, 204, 205, 206, 207,
            300, 301, 302, 303, 304, 305, 307, 308,
            400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418,
            422, 423, 424, 426, 428, 429, 431, 451,
            500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511
        ]

        # The tuple is (lower_bound, upper_bound) where lower_bound is inclusive and upper_bound is exclusive
        self.code_types = {
            "info": (100, 200),
            "success": (200, 300),
            "redirect": (300, 400),
            "client_error": (400, 500),
            "server_error": (500, 600)
        }

    def get_all_codes(self):
        """
        Return the complete list of HTTP codes
        
        Returns:
            list of int: The HTTP codes
        """
        return self.codes

    def get_codes_by_type(self, type_name):
        """
        Return a filtered list of HTTP codes by a given type
        
        Parameters:
            type_name (str): The category to filter by
        
        Returns:
            list of int: List of HTTP codes matching the type
        """
        t = type_name.strip().lower()
        if t in self.code_types:
            lower, upper = self.code_types[t]
            return [code for code in self.codes if lower <= code < upper]
        else:
            return []

    def get_all_types(self):
        """
        Return a dictionary of all available HTTP code types along with their corresponding codes
        
        Returns:
            dict: A dictionary with type names as keys and lists of codes as values
        """
        return {type_name: [code for code in self.codes if lower <= code < upper]
                for type_name, (lower, upper) in self.code_types.items()}

    def get_type_names(self):
        """
        Return a list of HTTP code type names
        
        Returns:
            list of str: The list of type names
        """
        return list(self.code_types.keys())
    
    def get_random_code(self, types=None):
        """
        Return a random HTTP code
        If a list of type names is provided, the code is selected only from those types.
        
        Parameters:
            types (list of str, optional): A list of type names 
        
        Returns:
            int: A random HTTP code from the specified types or from all codes if no valid types are provided
        """
        if types is not None:
            valid_types = [t.strip().lower() for t in types if t.strip().lower() in self.code_types]
            selected_codes = []
            for type in valid_types:
                lower, upper = self.code_types[type]
                selected_codes.extend([code for code in self.codes if lower <= code < upper])
            if not selected_codes:
                selected_codes = self.codes
            return random.choice(selected_codes)
        return random.choice(self.codes)
    
    def get_type_by_code(self, code):
        """
        Return the type name for a given HTTP code based on the configured code_types
        
        Parameters:
            code (int): The HTTP status code
        
        Returns:
            str or None: The type name if the code exists otherwise None
        """
        for type_name, (lower, upper) in self.code_types.items():
            if lower <= code < upper:
                return type_name
        return None
    
    def code_is_error(self, code):
        """
        Check if the given HTTP code represents a client or server error

        Parameters:
            code (int): The HTTP status code

        Returns:
            bool: True if the code is a client or server error, False otherwise
        """
        type_name = self.get_type_by_code(code)
        return type_name in ("client_error", "server_error")
    
    def is_valid_code(self, code):
        """
        Check if the given HTTP is a valid HTTP status code

        Parameters:
            code (int): The HTTP status code

        Returns:
            bool: True if the code is valid, False otherwise
        """
        return code in self.codes
    