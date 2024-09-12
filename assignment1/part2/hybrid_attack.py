import hashlib
import argparse

def hash_password(password, algorithm='sha256'):
    """Hash a password using a specified algorithm and return the hexadecimal digest."""
    if algorithm == 'sha256':
        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        return sha256.hexdigest()
    elif algorithm == 'sha1':
        sha1 = hashlib.sha1()
        sha1.update(password.encode('utf-8'))
        return sha1.hexdigest()
    
def load_hashes(file_path):
    """Load hashes from a file into a set."""
    with open(file_path, 'r') as f:
        return set(line.strip() for line in f)

def load_dictionary(file_path):
    """Load potential passwords from a dictionary file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f]

def check_password_variants(password, hashes,algorithm, out_file, write):
    """Check a password against hashes with original, 2-digit prefix, and 2-digit prefix + 1-digit postfix."""
    match_count = 0
    # Check original password
    hashed_password = hash_password(password,algorithm)
    if hashed_password in hashes:
        if write:
            out_file.write(f"{hashed_password} {password}\n")
        print(f"Match found: {password}")
        match_count += 1
    
    # Check 2-digit prefix
    for prefix in range(100):  
        prefixed_password = f"{prefix}{password}"
        hashed_password = hash_password(prefixed_password,algorithm)
        if hashed_password in hashes:
            if write:
                out_file.write(f"{hashed_password} {prefixed_password}\n")
            print(f"Match found: {prefixed_password}")
            match_count += 1
        
    # Check 2-digit prefix + 1-digit postfix
    for prefix in range(100): 
        for postfix in range(10):  
            modified_password = f"{prefix}{password}{postfix}"
            hashed_password = hash_password(modified_password,algorithm)
            if hashed_password in hashes:
                if write:
                    out_file.write(f"{hashed_password} {modified_password}\n")
                print(f"Match found: {modified_password}")
                match_count += 1

    return match_count

def hybrid_attack(hash_file, dictionary_file, algorithm, output_file, max_lines=100):
    """Perform a hybrid attack by applying modifications to dictionary words."""
    hashes = load_hashes(hash_file)
    dictionary = load_dictionary(dictionary_file)
    num_hashes = len(hashes)

    with open(output_file, 'w', encoding='utf-8') as out_file:
        total_matches = 0
        for password in dictionary:
            matches = check_password_variants(password, hashes, algorithm,out_file, total_matches < max_lines)
            total_matches += matches
            
    print(f"Hybrid attack complete. {total_matches} matches found. Percentage of hashes cracked: {total_matches / num_hashes * 100:.2f}%")


def main():
    # hash_file = 'formspring/formspring.txt'  # File containing SHA-256 hashes
    # dictionary_file = '7-more-passwords.txt'  # File containing dictionary of possible passwords
    # output_file = 'formspring_matches.txt'  # Output file to save matches

    # hash_file = 'linkedin/SHA1.txt' # File containing SHA-1 hashes
    # dictionary_file = '7-more-passwords.txt'  # File containing dictionary of possible passwords
    # output_file = 'linkedin_matches.txt'  # Output file to save matches

    parser = argparse.ArgumentParser(description="Perform a hybrid dictionary attack on provided hashes.")
    
    parser.add_argument('hash_file', type=str, help="Path to the input file containing hashes.")
    parser.add_argument('output_file', type=str, help="Path to the output file where results will be written.")
    parser.add_argument('algorithm', type=str, default='sha256', choices=['sha256', 'sha1'],help="Hashing algorithm to use (default: 'sha256').")
    parser.add_argument('-d', '--dictionary', type=str, default='7-more-passwords.txt', 
                        help="Path to the dictionary file (default: '7-more-passwords.txt').")
    parser.add_argument('-m', '--max-lines', type=int, default=100, 
                        help="Maximum number of matches to write to the output file (default: 100).")
    
    args = parser.parse_args()

     # Call the hybrid_attack function with the arguments from the command line
    hybrid_attack(args.hash_file, args.dictionary, args.algorithm, args.output_file, args.max_lines)

if __name__ == '__main__':
    main()