# NMAP DECOY LAB - KALI LINUX INSTALLATION GUIDE

**Cyberpunk Terminal UI for Nmap Decoy Scans**  
Built for Debian-based systems (Kali Linux, Parrot OS)  
Created by Rax Ontto

---

## OVERVIEW

This is a real Python CLI tool that runs directly in your Kali terminal. It provides:
- Cyberpunk aesthetic terminal UI using the `rich` library
- Safe nmap wrapper with decoy node injection (`-D RND:N`)
- Input validation (no arbitrary spoofing, lab networks only)
- Decoy count limits (1–10, default 3)
- Default port range 1–200
- Verbose mode (default ON)
- Report generation

---

## STEP 1: VERIFY KALI IS UPDATED

```bash
sudo apt update
sudo apt upgrade -y
```

---

## STEP 2: INSTALL NMAP (if not already present)

Nmap is usually pre-installed in Kali, but verify:

```bash
nmap --version
```

If not installed:

```bash
sudo apt install nmap -y
```

---

## STEP 3: INSTALL PYTHON 3 & PIP

Verify Python 3 is installed:

```bash
python3 --version
pip3 --version
```

If missing:

```bash
sudo apt install python3 python3-pip -y
```

---

## STEP 4: DOWNLOAD & SETUP THE TOOL

### Option A: Copy files directly (if you have them)

Create a working directory:

```bash
mkdir -p ~/decoy_lab
cd ~/decoy_lab
```

Copy `decoy_lab.py` and `requirements.txt` into `~/decoy_lab/`

### Option B: Create from scratch

```bash
mkdir -p ~/decoy_lab
cd ~/decoy_lab
```

Then create the two files (use a text editor or copy-paste):

**decoy_lab.py** — the main script  
**requirements.txt** — dependencies

---

## STEP 5: INSTALL DEPENDENCIES

```bash
cd ~/decoy_lab
pip3 install --break-system-packages -r requirements.txt
```

**Why `--break-system-packages`?**  
Kali is a system tool and locks pip to "managed environments." This flag allows installation into the global Python.

Alternative (using venv, optional but cleaner):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then whenever you run the tool, activate the venv first:
```bash
cd ~/decoy_lab
source venv/bin/activate
python3 decoy_lab.py
```

---

## STEP 6: MAKE THE SCRIPT EXECUTABLE

```bash
chmod +x ~/decoy_lab/decoy_lab.py
```

---

## STEP 7: RUN THE TOOL

### From anywhere:

```bash
cd ~/decoy_lab
sudo python3 decoy_lab.py
```

**Why `sudo`?**  
Nmap decoy mode (`-D RND:N`) requires raw socket access, which needs root privileges.

### Create an alias (optional, for convenience):

Add this to `~/.bashrc`:

```bash
alias decoy='cd ~/decoy_lab && sudo python3 decoy_lab.py'
```

Then reload:

```bash
source ~/.bashrc
```

Now you can run from anywhere:

```bash
decoy
```

---

## STEP 8: FIRST RUN WALKTHROUGH

When you launch, you'll see:

1. **Boot Sequence** — System initialization animation (plays once)
2. **Main Menu** — 5 options:
   - `[01]` DECOY SCAN — Execute a lab scan
   - `[02]` TRACE ANALYZER — Analyze Wireshark captures
   - `[03]` NMAP ANALYZER — Parse saved nmap output
   - `[04]` SYSTEM STATUS — View config & constraints
   - `[00]` EXIT — Quit

### Running a DECOY SCAN:

1. **Enter target** — IP (e.g., `192.168.1.100`) or domain (lab only)
2. **Select decoy count** — 1–10 nodes (default 3)
3. **Choose port range** — Presets or custom (default `1-200`)
4. **Verbose mode** — ON or OFF (default ON)
5. **Authorization** — Confirm you own/are authorized for this target
6. **Execute** — Watch the scan in real-time
7. **View results** — Open ports, services, and detailed telemetry

Reports are automatically saved to `~/decoy_reports/`

---

## SECURITY NOTES

✅ **ALLOWED:**
- Decoy scan on authorized lab networks
- `-D RND:N` injection (random decoy IPs)
- Custom port ranges
- Verbose telemetry output
- Multiple scans

❌ **BLOCKED:**
- Arbitrary `-S` source spoofing
- Exploit automation
- Scanning outside lab scope
- Decoy count >10
- Anonymous mode without authorization

---

## TROUBLESHOOTING

### "nmap: command not found"
```bash
sudo apt install nmap -y
```

### "Permission denied" when running
```bash
sudo python3 decoy_lab.py
# or
sudo chmod +x ~/decoy_lab/decoy_lab.py
```

### "ModuleNotFoundError: No module named 'rich'"
```bash
pip3 install --break-system-packages rich
# or if using venv:
source ~/decoy_lab/venv/bin/activate
pip install rich
```

### Nmap scan hangs or times out
- Reduce port range (`1-100` instead of `1-65535`)
- Use fewer decoys (`1-3` instead of `10`)
- Check your network connectivity
- Verify target is reachable: `ping <target>`

### "Cannot assign requested address" during scan
- Ensure you're running with `sudo`
- Check your internet interface: `ip a`
- Try a smaller decoy set

---

## FILE STRUCTURE

After setup, your directory should look like:

```
~/decoy_lab/
├── decoy_lab.py               # Main script
├── requirements.txt            # Dependencies
├── KALI_INSTALL_GUIDE.md      # This file
├── venv/                       # (optional, if using venv)
└── ~/decoy_reports/            # Auto-created, scan reports

```

---

## UPDATING THE TOOL

```bash
cd ~/decoy_lab
# Replace decoy_lab.py with the new version
pip3 install --upgrade --break-system-packages rich
```

---

## UNINSTALLING

```bash
rm -rf ~/decoy_lab
rm -rf ~/decoy_reports
# (optional) Remove alias from ~/.bashrc
```

---

## USAGE EXAMPLE

```bash
$ sudo python3 decoy_lab.py

[Boot sequence plays…]

DECOY NETWORK LAB
NMAP OPERATIONS CONSOLE  ◈  v1.0.0  ◈  BY RAX ONTTO

SELECT OPERATION:
  [01] ◈ DECOY SCAN           Execute authorized lab scan
  [02] ◈ TRACE ANALYZER       Analyze packet evidence
  [03] ◈ NMAP ANALYZER        Parse saved scan output
  [04] ◈ SYSTEM STATUS        Inspect environment
  [00] ◈ EXIT                 Close console

  SELECT OPERATION: 01

[TARGET ACQUISITION screen]
  TARGET ──► 192.168.1.100

[DECOY MATRIX screen]
  Select: 05

[PORT MATRIX screen]
  PORTS ──► 1-200

[VERBOSE MODE screen]
  VERBOSE ──► Y

[AUTHORIZATION GATE screen]
  CONFIRM ──► Y

[LIVE OPERATION – nmap -D RND:5 -p 1-200 192.168.1.100]

STATUS: ████████░░ 87%

[Results display with open ports, duration, etc.]

Report saved: /home/user/decoy_reports/scan_20240101_120530.txt
```

---

## SUPPORT & CUSTOMIZATION

**To modify the tool:**
- Edit `decoy_lab.py` in any text editor
- Change colors: Search for `GREEN`, `CYAN`, `MAGENTA`, etc.
- Modify port defaults: Line ~340, `ports_range`
- Change decoy limit: Line ~280, change `range(1, 11)` to your preference

**To report issues:**
- Ensure nmap is installed and accessible
- Run with `sudo`
- Check that `rich` is installed: `pip3 show rich`
- Verify Kali is up-to-date

---

## CREDITS

**Created by:** Rax Ontto  
**Built for:** Kali Linux, Parrot OS (Debian-based)  
**UI Framework:** Rich (Python)  
**Security Tool:** Nmap  
**License:** Lab/Educational Use

---

**AUTHORIZED SECURITY LAB ONLY**  
This tool is intended for authorized network testing in controlled lab environments.  
Unauthorized port scanning may be illegal in your jurisdiction.

