import hashlib


def hash_password(password):
    """Hash a password using SHA-1 and return the hexadecimal digest."""
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    return sha1.hexdigest()

def load_hashes(file_path):
    """Load hashes from a file into a set."""
    with open(file_path, 'r') as f:
        return set(line.strip() for line in f)

def load_dictionary(file_path):
    """Load potential passwords from a dictionary file."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]

def dictionary_attack(hash_file, dictionary_file, output_file, max_lines=100):
    """Perform a dictionary attack and write up to a specified number of matches to an output file."""
    hashes = load_hashes(hash_file)
    dictionary = load_dictionary(dictionary_file)
    
    with open(output_file, 'w') as out_file:
        match_count = 0
        for password in dictionary:
            hashed_password = hash_password(password)
            if hashed_password in hashes:
                if match_count < max_lines:
                    out_file.write(f"{hashed_password} {password}\n")
                print(f"Match found: {password}")
                match_count += 1
    
    print(f"Dictionary attack complete. {match_count} matches found.")


dictionary_file = '1000000-password-seclists.txt'  # File containing dictionary of possible passwords

dictionary_attack('linkedin/SHA1.txt', dictionary_file, "linkedin_matches.txt")