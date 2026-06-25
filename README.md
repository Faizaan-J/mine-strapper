<div align="center">
    <img src="./assets/logo/minestrapper-logo.png" width="180" height="180" />
    <h1>Minestrapper</h1>
    <p>A bootstrapper for Minecraft Java Edition Servers
</div>

## About
Rather than building full Java plugins or mods, this project lets you tap into the server’s state and other lifecycle events, and add custom functionality directly in Python.

That means small features can be added without the overhead of a mod loader (e.g. [Fabric](https://fabricmc.net/), [Forge](https://files.minecraftforge.net/net/minecraftforge/forge/)) or plugin loader (e.g. [Paper](https://papermc.io/), [Spigot](https://www.spigotmc.org/)), while keeping the server in its vanilla form.

> [!NOTE] 
> Feel free to still use your favorite mods or plugins alongside it if you want! Minestrapper mainly serves for smaller, simpler features.

## Current Features
- Config Handling
  - Contains a class for managing configuration files of both Minestrapper and Minecraft.
  - Minestrapper config uses a file named `Config.json` in a `/minestrapper` directory relative to the root of the Minecraft Server.
  - Allows for direct editing of `server.properties`.
- State Handling
  - Contains a class for getting the current state of the server based on the server output.
  - Tracks the following states: `STARTING`, `RUNNING`, `PAUSED`, `STOPPING`, `STOPPED`.
- Periodic Callbacks
  - A lifecycle function that runs every 20ms.
  - Used for things that need to happen constantly.
  - Mainly isn't used in preference of lifecycle events.
- New Line Callbacks
  - A lifecycle function that runs everytime a new line is sent from the Minecraft Server process
- Logger
  - Prints out stuff both from forwarding logs from the Minecraft process and also custom logs from Minestrapper.
  - Keeps Minestrapper specific logs visually consistent with Minecraft Server logs (e.g. "[19:48:06] [Minestrapper/INFO]: Initialized Minestrapper Logger successfully.")
  - Logs to a file named `latest-minestrapper.log` and then replaces the vanilla `latest.log` with it when the server stops.
  - Provides `transformers` to modify each logged line to the output as needed. 
- Built-in features:
  - "State Styles"
    - Updates the terminal title and text color based on the server's current state.
    - Makes it easier to see whether the server is starting, running, paused, stopping, or stopped.
  - "Server Resource Pack"
    - Includes a lightweight HTTP server for serving a server resource pack.
    - Removes the need for an external hosting site for the pack.
    - Keeps resource pack delivery self-contained within the server setup.

## Potential Future Features
- Backups: Let the owner integrate save backups everytime the server closes locally. It can either be done locally only, with cloud services, or even both.
- Remote Panels: Allow the owner along with anyone else authorized to remotely turn on and off the server. Only the owner will be able to view logs and run commands however.
- Custom Commands: Add your own admin commands that can trigger multiple Minecraft commands or even run Python code.

## Installation Guide
1. Install Python at [https://www.python.org/](https://www.python.org/) (>=3.1).
2. Go to your Minecraft Server directory.
3. Make a directory exactly named `minestrapper` and change directory to it.
```
mkdir minestrapper && cd minestrapper
```

4. Make a new Python environment.

**Windows:**
```
python -m venv .venv
```

**MacOS / Linux:**
```
python3 -m venv .venv
```

5. Activate the environment.

**Windows:**
```
.\.venv\Scripts\activate
```

**MacOS / Linux:**
```
source .venv/bin/activate
```

6. Install the `minestrapper` package.
```
pip install minestrapper
```

7. Create a file exactly named `Config.json` and edit to your liking.
```json
{
  "$schema": "https://raw.githubusercontent.com/Faizaan-J/mine-strapper/refs/heads/main/Config.schema.json"
}
```
> [!NOTE]
> The schema will help you fill out the file so it's recommended to use some kind of app that can read JSON schemas to edit the file easier. There are numerous required fields that you must fill out.

8. Make an entry point file inside the `minestrapper` directory.

**Example:**
```python
from pathlib import Path

from minestrapper import Server

if __name__ == "__main__":
    server = Server(path=Path.cwd().parent)
    server.start_server()

    server.wait_loop()

```

## Important Notes
- You still need to do any necessary port forwarding yourself.

## License
MineStrapper is released under the [MIT License](./LICENSE).  
Feel free to use, modify, and share.
