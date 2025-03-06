import aiohttp
import asyncio
import json

async def stream_response():
    url = "https://api.ngc.nvidia.com/v2/predict/models/qc69jvmznzxy/llama-3_1-nemotron-70b-instruct"
    headers = {
        "authority": "api.ngc.nvidia.com",
        "method": "POST",
        "path": "/v2/predict/models/qc69jvmznzxy/llama-3_1-nemotron-70b-instruct",
        "scheme": "https",
        "accept": "text/event-stream",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "622",  # Correct content length for the provided payload
        "content-type": "application/json",
        "nv-captcha-token": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXNza2V5IjoiUmJwM25oeWpvWjAvdVRDaXgrdlRQYWwxVENFWkxSbVVxaWc2RWdGZzBwNzdqTG04T25TSzk5eThPajJoSEZsbTFCekc0bGJwZkkvekY3UUhLeUx1Q1pxQWJLZnc4aWZ1OWk5UEd6cVVyelV4Y3BHNVlOc05tWStIRXJ0NUtEQ2s1a3JLUGRUckdkM2hpaFl3T3AwRm1XdDFnN1oyRnU5TW81Y0NwMmlkWXE5My9nSGFoUXQzaDBkSDJqQysxSVlmWUVOeUxXdWw0d3N6TzJDK0Q5RHBvVVAyT1YvN0pMTzlHTGlmZEduV2phd2pYZThjNkhQVHJRSWg0TVA5MVBodUpmRU9uVTU0S2VLaTJITVduaXNBU2QzamVpcFRLWEovUmJ1M0twanh3UUZ1ZVlFdGFYaVZTakpPVXV3YzUrTzF6SklVVXlqajNkcjFqa1haNWt1OGxRS1pvdHU1c21XVHh5b05SSWk0TlNmTHVzL3dVcStvRkkyQ3JaUEptdGY1ZVdVcWZ3dFRLejlZMjd6dWs5UHJaeE51b0w2UkxPMWwySWxhVnhQWGt3MlNpSmlrR2JkaVcvYlVKcksxd01vWGlZandHQ3dNekR1eTlhbFlHbmYzTy9KUUdvUzFsV3Y5U2g1N3hZWjN5UjB5YitSZzFvWnNKSEUyV2tadWEwSFA3Q2hncTFadWV6cHcxdVh5WXJxSmJMYjF0N0dtN2hPZkVYamdCY0psQWYxL2ltd3cvTHh5andQMTZMMSsxd2duMHNkcHA0R2JTYmRwMWJMQzVnZ0dGbGhQWG04RnFyajA0UWwxSGhyajZTYURrNVdPYlBNMTdvNXZzdWlYNENPR0NVQkJUQ2EzVGtCSERpemtlOHAycDB6UWVPQlFGczIxSTV5TWJzRE54N0x5Mi9vL3pZc0xETjIreDh6QUdMdW9DdGxBaEsxUEZ2eTFrWGh0ZHBlQUU4Y05SVHZSNllIMDRkWjVuS25NNXk2c3FIWlhNSUhKN2Z3TlNvYVBiOENEeHN2d1pkdWpwbXpFb1pBU3FxLzFLb2tsbUZBYTlJZW9weVBDc3E5TWtiS2dzNWErR2VvRkZabmsvbXl4OVowQm8rK3FkSVlta1JpVW9PL2J1NlVhOWZNMFlDaXNJYlFnOWVTZTNUSitnRTFUb1RDbGpmRzltZzJqdHNlcUpRM2pQMW1OZUtJVVo5QktpWHR2RG81SGt0a1pVaklkTURkY0F3Q3ZlNlpLS0VYdXZSemlUWkVVVlBCM2M5R2svMHF6Zlc4Yyt1NnVHdVltd0RJbm1MMGdlbnZjcEU0SXh1Z1NKNGlmeHdBM3Zza1kvNkxqd3BpQTJjTXozWEdvY2xKUEgyS2RRMUNjWTZZSmZNVWdleXlNMGROM0I4bFpIQnN0OWlmeUJnbjFpNCtZVnBpbzluRHJkZlFWOVJ3RHVnU3E5eFd1MnVFdTkzcyttQ1lFTStmRXQybEZLUVJDZkVQa3dyenJJT054QUZlSC9ZNGMxZEQ5dS9jNmkzWkNPckROVVVEclhhR3h4cnN6OWtQWFpEVjRSRElZNVc3dnlsd1UzMWJhUEppTGRwMWVrayttN0x3akNMYVJRa1htRGZ2TGVweGo4WEhWOFpiSDVyV09HWXZ0dXEwb1RTL3JnRHVZcXA4TlBsWjBSVVlXdjhHWWV6clNmVHVUNHpqbmZoRXMzWWZxY2pRYjg5TEYzdURaZjgzNlZONFJCZHBEdkdKUXJESHVjSThKTVpTeGM5YWowWVlCMlgyeHZSeXZRaW1TTHB0R1VaUlRGemZ3bkVTWVZ2aVJVTXZTaE5SeUFBYUR5OW9lMFlEZXpGTjJMYkUrelNXZmwyRmxJQVc5NldYR1ZSN2srRGp6NkhHRXdqZERJVzRUcE5FPSIsImV4cCI6MTc0MDk4MDc2OSwic2hhcmRfaWQiOjUzNTc2NTU5LCJrciI6IjRhNTA2MGU4IiwicGQiOjB9.5VZKHzK_Yx-g7B64odRC1tOrWeWuTRjaebnrc8RzTPQ",
        "nv-function-id": "9b96341b-9791-4db9-a00d-4e43aa192a39",
        "origin": "https://build.nvidia.com",
        "priority": "u=1, i",
        "referer": "https://build.nvidia.com/",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    }

    payload = {
        "model": "nvidia/llama-3.1-nemotron-70b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a limerick about the wonders of GPU computing."},
            {"role": "assistant", "content": "Here is a limerick about the wonders of GPU computing:\n\nThere once was a GPU so fine,\nWhose computing powers did shine.\nIt crunched with great zest,\nThrough tasks that were a test,\nAccelerating all, in its prime!"},
            {"role": "user", "content": "hello world"}
        ],
        "top_p": 0.7,
        "max_tokens": 1024,
        "seed": 42,
        "stop": None,
        "stream": True,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.5
    }


    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                async for chunk in response.content.iter_any():  # Iterate over data chunks
                    if chunk:
                        print(chunk.decode('utf-8', errors='ignore'), end='') # Decode and print each chunk

            else:
                print(f"Request failed with status: {response.status}")
                error_message = await response.text()
                print(f"Error message: {error_message}")

async def main():
    await stream_response()

if __name__ == "__main__":
    asyncio.run(main())