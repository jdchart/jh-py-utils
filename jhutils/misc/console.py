import sys

def print_progress_bar_colab(progress, total, post_message="", length=50):
    percent = progress / total
    filled_length = int(length * percent)
    bar = '█' * filled_length + '-' * (length - filled_length)
    
    # Print progress bar, ensuring the output is flushed
    sys.stdout.write(f'\r|{bar}| {percent:.1%} Complete {post_message}')
    sys.stdout.flush()  # Force print update in Colab
    
    if progress == total:
        print()  # Move to a new line at the end

        
def print_progress_bar(progress, total, post_message, length = 50):
    percent = progress / total
    filled_length = int(length * percent)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r|{bar}| {percent:.1%} Complete {post_message}', end='\r')
    if progress == total:
        print()