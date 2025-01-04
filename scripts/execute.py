import subprocess

async def execute_command(command):
    try:
        # Execute the command and get the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)
