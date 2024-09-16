import hashlib
import argparse

def hash_password(password, algorithm):
    """Hash a password using the specified algorithm and return the hexadecimal digest."""
    if algorithm == 'sha256':
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(password.encode('utf-8')).hexdigest()

def load_hashes(file_path):
    """Load hashes from a file into a set."""
    with open(file_path, 'r') as f:
        return set(line.strip() for line in f)


def check_password_variants(password, hashes, algorithm, out_file, total_matches, max_lines):
    """
    Check a password against hashes for:
    - The original password
    - A password with a 2-digit prefix
    - A password with a 2-digit prefix + 1-digit postfix
    """
    match_count = 0

    # Check original password
    hashed_password = hash_password(password, algorithm)
    if hashed_password in hashes:
        match_count += 1
        if total_matches <= max_lines:
            if total_matches == max_lines - 1:
                out_file.write(f"{hashed_password} {password}")
            else:
                out_file.write(f"{hashed_password} {password}\n")
        print(f"Match found: {password}")
        
    
    # Check 2-digit prefix variants
    for prefix in range(100):
        prefixed_password = f"{prefix:02}{password}"
        hashed_password = hash_password(prefixed_password, algorithm)
        if hashed_password in hashes:
            match_count += 1
            if total_matches <= max_lines:
                if total_matches == max_lines - 1:
                    out_file.write(f"{hashed_password} {prefixed_password}")
                else:
                    out_file.write(f"{hashed_password} {prefixed_password}\n")
            print(f"Match found: {prefixed_password}")
            

    # Check 2-digit prefix + 1-digit postfix variants
    for prefix in range(100):
        for postfix in range(10):
            modified_password = f"{prefix:02}{password}{postfix}"
            hashed_password = hash_password(modified_password, algorithm)
            if hashed_password in hashes:
                match_count += 1
                if total_matches <= max_lines:
                    if total_matches == max_lines - 1:
                        out_file.write(f"{hashed_password} {modified_password}")
                    else:
                         out_file.write(f"{hashed_password} {modified_password}\n")
                print(f"Match found: {modified_password}")

    return match_count

def hybrid_attack(hash_file, dictionary_file, algorithm, output_file, max_lines=100, early_stop=False):
    """Perform a hybrid dictionary attack by checking password variants against hashes."""
    hashes = load_hashes(hash_file)
    total_matches = 0
    num_hashes = len(hashes)

    with open(dictionary_file, 'r', encoding='utf-8', errors='ignore') as in_file, \
         open(output_file, 'w', encoding='utf-8') as out_file:
        for password in in_file:
            password = password.strip()
            matches = check_password_variants(password, hashes, algorithm, out_file, total_matches, max_lines)
            total_matches += matches
            if early_stop and total_matches >= max_lines:
                print(f"Hybrid attack stopped early. {total_matches} matches found.")
                break
    if not early_stop:
        print(f"Hybrid attack complete. {total_matches} matches found. "
          f"Percentage of hashes cracked: {total_matches / num_hashes * 100:.2f}%")

def main():
    """Main function to parse arguments and run the hybrid attack."""
    parser = argparse.ArgumentParser(description="Perform a hybrid dictionary attack on provided hashes.")
    parser.add_argument('hash_file', type=str, help="Path to the input file containing hashes.")
    parser.add_argument('output_file', type=str, help="Path to the output file where results will be written.")
    parser.add_argument('algorithm', type=str, choices=['sha256', 'sha1'],
                        help="Hashing algorithm to use.")
    parser.add_argument('-d', '--dictionary', type=str, default='7-more-passwords.txt',
                        help="Path to the dictionary file (default: '7-more-passwords.txt').")
    parser.add_argument('-m', '--max-lines', type=int, default=100,
                        help="Maximum number of matches to write to the output file (default: 100).")
    parser.add_argument('--early-stop', action='store_true', help='Enable early stopping')

    args = parser.parse_args()

    # Call the hybrid_attack function with the parsed arguments
    hybrid_attack(args.hash_file, args.dictionary, args.algorithm, args.output_file, args.max_lines, args.early_stop)

if __name__ == '__main__':
    main()
