import asyncio
import aiohttp
import aiofiles
import os, time, glob
from urllib.parse import urlparse
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

#Asyncio part

# start = time.perf_counter()
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

# end = time.perf_counter()

async def main():
    async with aiohttp.ClientSession() as session:
        # Read URLs
        with open("input_urls.txt", "r") as f:
            urls = [line.strip() for line in f if line.strip()]

        # Optional: limit concurrency with semaphore
        semaphore = asyncio.Semaphore(5)  # max 5 downloads at a time

        async def sem_download(url, index):
            async with semaphore:
                await download_image(session, url, index)

        tasks = [sem_download(url, i) for i, url in enumerate(urls, start=1)]
        await asyncio.gather(*tasks)


#Threading part

saved_folder = "saved_formats"
os.makedirs(saved_folder, exist_ok=True)

formats = ["png", "jpeg", "webp"]

def save_in_diff_formats(file_path):

    try:
        img = Image.open(file_path)
        basename = os.path.splitext(os.path.basename(file_path))[0]

        for format in formats:
            save_path = os.path.join(saved_folder, f"{basename}.{format}")
            img.save(save_path, format)
            print(f"Saved {save_path}")

        except Exception as ex:
            print(f"Failed to save {file_path}: {ex}")


def thread_save():
    downloaded_files = glob.glob(os.path.join(download_folder, "*"))

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(save_in_diff_formats, downloaded_files)




    # time_taken = time.perf_counter() - start
    # print(f"Downloaded {len(urls)} urls in {time_taken} seconds")



if __name__ == "__main__":
    asyncio.run(main())
    thread_save()
