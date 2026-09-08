import crypt
import sys

def main(args):
    """
    Hash a password using the crypt function.
    """
    if len(args) < 2:
        print(f"Usage: {args[0]} <plaintext password> <salt value>")
        return 1
    
    print(f'password "{args[1]}" with salt "{args[2]}" ', end='')
    print(f'hashes to ==> {crypt.crypt(args[1], args[2])}')
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))