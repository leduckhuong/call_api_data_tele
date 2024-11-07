async def progress_callback(current, total):
    percentage = (current / total) * 100
    print(f'Downloading file: {current}/{total} bytes ({percentage:.2f}%)')