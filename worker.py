import httpx
import asyncio
import schedule
import time

async def get_pxdata():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/")
        if response.status_code == 200:
            pxdata = response.text
            return pxdata
        else:
            print("Error:", response.status_code)
            return None

def save_pxdata_to_file(pxdata):
    if pxdata:
        with open("pxdata.txt", "a") as file:
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {pxdata}\n")

def fetch_and_save_data():
    pxdata = asyncio.run(get_pxdata())
    if pxdata:
        save_pxdata_to_file(pxdata)

schedule.every(5).seconds.do(fetch_and_save_data)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()