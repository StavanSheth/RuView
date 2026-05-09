# RuView — Self README (How to Run Locally via CMD)

> Quick personal reference for launching the RuView sensing backend and dashboard from CMD on Windows.

---

## Project Structure (What Matters)

```
C:\Projects\RuView\
│
├── Launch-RuView.bat                        ← One-click launcher (double-click or run from CMD)
│
├── rust-port\
│   └── wifi-densepose-rs\                   ← Rust backend workspace
│       └── crates\
│           └── wifi-densepose-sensing-server ← The main server crate
│
└── ui\                                      ← Static frontend (HTML/JS/CSS via Vite)
    ├── index.html                           ← Main dashboard
    ├── package.json
    └── vite.config.js                       ← Dev server config (port 3000 by default)
```

---

## Prerequisites

Make sure the following are installed before running anything:

| Tool      | Check Command         | Install From                        |
|-----------|-----------------------|-------------------------------------|
| Rust      | `rustc --version`     | https://rustup.rs                   |
| Cargo     | `cargo --version`     | Comes with Rust                     |
| Node.js   | `node --version`      | https://nodejs.org                  |
| npm       | `npm --version`       | Comes with Node.js                  |

---

## Option 1 — One-Click Launch (Simplest)

Open CMD and run:

```cmd
cd C:\Projects\RuView
Launch-RuView.bat
```

Or just **double-click** `Launch-RuView.bat` in File Explorer.

This will:
1. Build and start the Rust backend on **port 3005**
2. Wait 5 seconds for it to initialize
3. Auto-open the dashboard at `http://localhost:3005/ui/index.html`

> **Note:** The terminal window running `cargo` must stay open. You can close the launcher window after it finishes.

---

## Option 2 — Manual CMD Launch (Step by Step)

Use this method when you need more control or want to run components separately.

### Step 1 — Start the Rust Backend

Open a **new CMD window** and run:

```cmd
cd C:\Projects\RuView\rust-port\wifi-densepose-rs

cargo run -p wifi-densepose-sensing-server -- --http-port 3005 --source esp32 --ui-path "C:\Projects\RuView\ui"
```

Wait until you see a line like:
```
Listening on http://0.0.0.0:3005
```

> **Keep this CMD window open.** The server runs here.

### Step 2 — Open the Dashboard

Open a **second CMD window** and run:

```cmd
start http://localhost:3005/ui/index.html
```

Or just paste `http://localhost:3005/ui/index.html` directly into your browser.

---

## Option 3 — Run with Vite Dev Server (UI Hot Reload)

Use this when actively developing the UI and need live browser refresh.

### Step 1 — Start Rust Backend (same as above)

```cmd
cd C:\Projects\RuView\rust-port\wifi-densepose-rs

cargo run -p wifi-densepose-sensing-server -- --http-port 8000 --source esp32 --ui-path "C:\Projects\RuView\ui"
```

> Note: backend port changed to **8000** here so Vite can proxy to it.

### Step 2 — Start Vite Dev Server

Open a **second CMD window** and run:

```cmd
cd C:\Projects\RuView\ui

npm install

npm run dev
```

Vite will start on `http://localhost:3000` and proxy all `/api` and `/health` requests to the Rust backend at `http://localhost:8000`.

Open: `http://localhost:3000`

---

## Changing the Port

### Change the Backend Port

The backend port is set via the `--http-port` flag at runtime. Simply change the number:

```cmd
cargo run -p wifi-densepose-sensing-server -- --http-port 4000 --source esp32 --ui-path "C:\Projects\RuView\ui"
```

Then open: `http://localhost:4000/ui/index.html`

To make this permanent, edit **`Launch-RuView.bat`** (line 19):

```bat
:: Change 3005 to your desired port
start "" "cargo" run -p wifi-densepose-sensing-server -- --http-port 3005 --source esp32 --ui-path "C:\Projects\RuView\ui"
```

Also update the dashboard URL on **line 25**:

```bat
start http://localhost:3005/ui/index.html
```

### Change the Vite Dev Server Port

Edit **`C:\Projects\RuView\ui\vite.config.js`**:

```js
export default defineConfig({
  server: {
    host: true,
    port: 3000,        // <-- Change this to your desired port (e.g. 4200)
    proxy: {
      '/api': {
        target: 'http://localhost:8000',   // <-- Must match your backend --http-port
        changeOrigin: true,
        ws: true
      },
      '/health': {
        target: 'http://localhost:8000',   // <-- Must match your backend --http-port
        changeOrigin: true
      }
    }
  }
})
```

Then restart with `npm run dev`.

---

## Port Reference Table

| Service              | Default Port | How to Change                          |
|----------------------|-------------|----------------------------------------|
| Rust backend         | `3005`      | `--http-port <PORT>` flag in cargo run |
| Vite dev server      | `3000`      | `port` field in `vite.config.js`       |
| Vite → backend proxy | `8000`      | `target` in `vite.config.js` proxy     |

---

## Hardware Prerequisites (ESP32)

Before running, make sure:

1. **Windows Mobile Hotspot is ON** — Name: `STAVAN-DESKSTOP 2500`
2. **Both ESP32 boards are plugged in** — They auto-connect to the hotspot
3. ESP32s stream data to `192.168.137.1` (your hotspot gateway IP)

> The ESP32 boards are already flashed and provisioned — no re-flashing needed unless you change your hotspot name/password.

---

## Re-Provisioning ESP32 (Only If Hotspot Changes)

If you change the hotspot name or password, run this in PowerShell with the ESP32 connected via USB:

```powershell
python firmware/esp32-csi-node/provision.py --port COM4 --ssid "Your_New_Network" --password "Your_Password" --target-ip 192.168.137.1 --node-id 1
```

Repeat with `--node-id 2` for the second board.

---

## Troubleshooting

| Problem                              | Fix                                                                 |
|--------------------------------------|---------------------------------------------------------------------|
| Port already in use                  | Change `--http-port` to a free port (e.g. `3006`, `4000`)          |
| `cargo` not found                    | Run `rustup update` or add `%USERPROFILE%\.cargo\bin` to your PATH |
| Dashboard loads but no data          | Check ESP32 boards are powered and hotspot is active                |
| `npm` not found                      | Install Node.js from https://nodejs.org                             |
| `Input redirection not supported`    | Harmless Windows CMD quirk — backend still runs fine                |
| Vite proxy errors (404 on /api)      | Ensure Rust backend is running and proxy `target` port matches      |
