import os

def create_headers(paper: bool=True, env_variable: str="TRADIER_SANDBOX_TOKEN") -> dict:
    """Create the headers for API requests

    :param paper: Paper or Live Trading, defaults to True
    :type paper: bool, optional
    :param env_variable: name of the env variable for the token generated by Tradier, defaults to ""
    :type env_variable: str, optional
    :return: header dict for use in API calls
    :rtype: dict
    """
    if paper:
        # do nothing
        pass
    else:
        # append the live token path
    
    token = os.environ.get(env_variable)
    return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }