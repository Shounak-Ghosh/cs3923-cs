import hashlib

def hash_password(password):
    """Hash a password using SHA-256 and return the hexadecimal digest."""
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

def load_hashes(file_path):
    """Load SHA-256 hashes from a file into a set."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return set(line.strip() for line in f)

def load_dictionary(file_path):
    """Load potential passwords from a dictionary file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f]

def check_password_variants(password, hashes, out_file, max_lines):
    """Check a password against hashes with original, 2-digit prefix, and 2-digit prefix + 1-digit postfix."""
    match_count = 0
    
    # Check original password
    hashed_password = hash_password(password)
    if hashed_password in hashes:
        if match_count < max_lines:
            out_file.write(f"{hashed_password} {password}\n")
        print(f"Match found: {password}")
        match_count += 1
    
    # Check 2-digit prefix
    for prefix in range(10, 100):  # 2-digit numbers from 10 to 99
        prefixed_password = f"{prefix}{password}"
        hashed_password = hash_password(prefixed_password)
        if hashed_password in hashes:
            if match_count < max_lines:
                out_file.write(f"{hashed_password} {prefixed_password}\n")
            print(f"Match found: {prefixed_password}")
            match_count += 1
        
    # Check 2-digit prefix + 1-digit postfix
    for prefix in range(10, 100):  # 2-digit numbers from 10 to 99
        for postfix in range(10):  # Single-digit numbers from 0 to 9
            modified_password = f"{prefix}{password}{postfix}"
            hashed_password = hash_password(modified_password)
            if hashed_password in hashes:
                if match_count < max_lines:
                    out_file.write(f"{hashed_password} {modified_password}\n")
                print(f"Match found: {modified_password}")
                match_count += 1

    return match_count

def hybrid_attack(hash_file, dictionary_file, output_file, max_lines=100):
    """Perform a hybrid attack by applying modifications to dictionary words."""
    hashes = load_hashes(hash_file)
    dictionary = load_dictionary(dictionary_file)
    
    with open(output_file, 'w', encoding='utf-8') as out_file:
        total_matches = 0
        for password in dictionary:
            matches = check_password_variants(password, hashes, out_file, max_lines)
            total_matches += matches
            if total_matches >= max_lines:
                break
            

    print(f"Hybrid attack complete. {total_matches} matches found.")

# # Usage
hash_file = 'formspring/formspring.txt'  # File containing SHA-256 hashes
dictionary_file = '7-more-passwords.txt'  # File containing dictionary of possible passwords
output_file = 'formspring_matches.txt'  # Output file to save matches

hybrid_attack(hash_file, dictionary_file, output_file)
