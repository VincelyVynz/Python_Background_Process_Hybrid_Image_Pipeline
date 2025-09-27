import asyncio, aiohttp, aiofiles
import os, time, glob
from urllib.parse import urlparse
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count

# --------------------- Asyncio part --------------------- #


download_folder = "downloaded"
os.makedirs(download_folder, exist_ok=True)

async def download_image(session, url, index):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                # Try to get extension from URL path
                path = urlparse(url).path
                ext = os.path.splitext(path)[1] or ".jpg"  # fallback to .jpg
                filename = os.path.join(download_folder, f"{index}{ext}")

                # Async write to file
                data = await response.read()
                async with aiofiles.open(filename, "wb") as f:
                    await f.write(data)

                print(f"Downloaded {filename}")
            else:
                print(f"Failed to download {url}: Status {response.status}")

    except aiohttp.ClientError as e:
        print(f"Failed to download {url}: {e}")



async def main():
    async with aiohttp.ClientSession() as session:
        # Read URLs
        with open("input_urls.txt", "r") as f:
            urls = [line.strip() for line in f if line.strip()]

        # limit concurrency with semaphore
        semaphore = asyncio.Semaphore(5)  # max 5 downloads at a time

        async def sem_download(url, index):
            async with semaphore:
                await download_image(session, url, index)

        tasks = [sem_download(url, i) for i, url in enumerate(urls, start=1)]
        await asyncio.gather(*tasks)


# --------------------- Threading part --------------------- #

saved_folder = "saved_formats"
os.makedirs(saved_folder, exist_ok=True)

formats = ["PNG", "JPEG", "WEBP"]

def save_in_diff_formats(file_path):

    try:
        img = Image.open(file_path)
        basename = os.path.splitext(os.path.basename(file_path))[0]

        for frmt in formats:
            save_path = os.path.join(saved_folder, f"{basename}.{frmt.lower()}")
            img.save(save_path, frmt)
            print(f"Saved {save_path}")

    except Exception as e:
            print(f"Failed to save {file_path}: {e}")


def thread_save():
    downloaded_files = glob.glob(os.path.join(download_folder, "*"))

    with ThreadPoolExecutor(max_workers=5) as executor:
        list(executor.map(save_in_diff_formats, downloaded_files))



# --------------------- Multiprocessing Part --------------------- #

processed_folder = "processed"
os.makedirs(processed_folder, exist_ok=True)
scale_factor  = 1.25
resample_method = Image.BICUBIC
process_count = cpu_count()

def process_image(file_path):
    try:
        img = Image.open(file_path)
        img_grayscale = img.convert("L")

        width, height = img_grayscale.size
        new_size = (int(width * scale_factor), int(height * scale_factor))
        img_resized = img_grayscale.resize(new_size, resample=resample_method)

        basename, ext = os.path.splitext(os.path.basename(file_path))
        save_path = os.path.join(processed_folder, f"{basename}_processed{ext}")
        img_resized.save(save_path)
        print(f"Processed and Saved {save_path}")

    except Exception as e:
        print(f"Failed to process {file_path}: {e}")


def multiprocessing_process():

    with Pool(process_count) as p:
        p.map(process_image, glob.glob(os.path.join(saved_folder, "*")))




if __name__ == "__main__":
    asyncio.run(main())
    thread_save()
    multiprocessing_process()
