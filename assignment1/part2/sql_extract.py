# Define the input and output file paths
input_file = 'yahoo/password.file'
output_file = 'yahoo_matches.txt'
max_lines = 100

# Open the input file and the output file
with open(input_file, 'r',errors='ignore') as infile, open(output_file, 'w') as outfile:
    # Iterate through each line in the input file
    match_count = 0
    for line in infile:
        # Split the line into fields using colon and strip any whitespace
        data = line.strip().split(':')
        
        # Check if the split line contains the expected 3 fields
        if len(data) == 3:
            user_id, user_name, clear_passwd = data
            user_id = user_id.strip()  # Clean up whitespace
            
            # Write the extracted data to the output file
            if user_id.isdigit():
                match_count += 1
                print(f"{user_id.strip()} {user_name.strip()} {clear_passwd.strip()}")
                if match_count <= max_lines:
                    if match_count == max_lines:
                        outfile.write(f"{user_id.strip()} {user_name.strip()} {clear_passwd.strip()}")
                    else:
                        outfile.write(f"{line.strip()} {clear_passwd.strip()}\n")
        
print(f"Data extracted and saved to {output_file}")
