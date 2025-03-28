def print_progress_bar(progress, total, post_message, length = 50):
    percent = progress / total
    filled_length = int(length * percent)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r|{bar}| {percent:.1%} Complete {post_message}', end='\r')
    if progress == total:
        print()