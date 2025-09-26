import asyncio, aiohttp, os

download_folder = "downloaded"
os.makedirs(download_folder, exist_ok=True)

async def download_images(session, url, index):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                ext = url.split(".")[-1].split("?")[0]
                filename = os.path.join(download_folder, f"{index}.{ext}")
                with open(filename, "wb") as f:
                    f.write(await response.read())
                print(f"Downloaded {filename}")
            else:
                print(f"Download of {url} failed: Status code: {response.status}")

    except aiohttp.ClientError as e:
        print(f"Download of {url} failed: {e}")

async def main():
    with open("input.txt", 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    async with aiohttp.ClientSession() as session:
        tasks = [download_images(session, url, i) for i, url in enumerate(urls, start=1)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
