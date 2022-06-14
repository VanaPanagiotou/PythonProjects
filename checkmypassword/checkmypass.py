import requests
import hashlib


def request_api_data(query_char):
    """The function uses Pwned Passwords endpoint with k-Anonymity model that allows a password to be searched for by partial hash.
    Only first 5 characters of a SHA-1 password hash are passed to the API.
    When a password hash with the same first 5 characters is found in the Pwned Passwords repository,
    the API will respond with an HTTP 200 and include the suffix of every hash beginning with the specified prefix,
    followed by a count of how many times it appears in the data set.
    A sample response for the hash prefix "21BD1" would be as follows:
    0018A45C4D1DEF81644B54AB7F969B88D65:1
    00D4F6E8FA6EECAD2A3AA415EEC418D38EC:2 etc.
    query_char: first 5 characters of the personal hashed password
    """

    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    """Separate returned hashes and count of how many times it appears in the data set
    and then search if the source hash exists in the returned hashes and if not found,
    the password does not exist in the data set.
    hashes: tailed hashes that API returned as matches with first 5 characters of personal's hashed password
    hash_to_check: tailed hash of personal password
    """

    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    """Create the hashed version of the personal password as required by the Pwned Passwords API.
    Split the hashed version of the personal password in the first 5 characters and the tail,
    get the API response with all matches and then search if the personal password has been pwned.
    password: personal password that user wants to test
    """
    # Check password if it exists in API response
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... You should probably change your password!')
        else:
            print(f'{password} was NOT found. Carry on!')
    return 'done!'


if __name__ == '__main__':
    file = open('passwords_to_be_checked.txt', 'r')  # txt files with passwords that we want to check
    lines = file.read().splitlines()
    main(lines)
