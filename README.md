# Nmap DecoyScan

**Cyberpunk Terminal UI for Nmap Decoy Scans**  
🔥 Real-time nmap wrapper with decoy node injection  
🖥️ Built for Kali Linux & Parrot OS (Debian-based)  
👤 Created by **Rax Ontto**

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-lab--use-orange)

---

## Overview

**Nmap DecoyScan** is a professional-grade terminal application that transforms nmap into a cyberpunk-styled security operations console. It automates decoy-based network scanning with visual feedback, input validation, and report generation.

### Key Features

- 🎯 **Decoy Injection** — Inject 1–10 random fake source IPs (`-D RND:N`) to obscure the real scanner
- 🔐 **Input Validation** — Authorized lab networks only; no arbitrary spoofing
- 🎨 **Cyberpunk UI** — Rich terminal styling with real-time progress tracking
- 📊 **Live Telemetry** — Watch port scans unfold with verbose nmap output
- 📄 **Report Generation** — Auto-save detailed scan reports
- ⚡ **Fast Setup** — Runs on any Kali/Parrot system with Python 3 + nmap

---

## Quick Start

### Prerequisites

- **Kali Linux** or **Parrot OS** (or any Debian-based system with sudo)
- **Nmap** installed (`apt install nmap`)
- **Python 3.7+** with pip

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/RaxingR/Nmap_DecoyScan.git
cd Nmap_DecoyScan

# 2. Install dependencies
pip3 install --break-system-packages -r requirements.txt

# 3. Make executable
chmod +x decoy_lab.py

# 4. Run it (requires sudo for raw socket access)
sudo python3 decoy_lab.py
```

### Create an Alias (Optional)

Add this to `~/.bashrc`:

```bash
alias decoy='cd ~/Nmap_DecoyScan && sudo python3 decoy_lab.py'
```

Reload: `source ~/.bashrc`

Then run from anywhere: `decoy`

---

## Usage

### Main Menu

```
DECOY NETWORK LAB
NMAP OPERATIONS CONSOLE  ◈  v1.0.0  ◈  BY RAX ONTTO

SELECT OPERATION:
  [01] ◈ DECOY SCAN           Execute authorized lab scan
  [02] ◈ TRACE ANALYZER       Analyze packet evidence
  [03] ◈ NMAP ANALYZER        Parse saved scan output
  [04] ◈ SYSTEM STATUS        Inspect environment
  [00] ◈ EXIT                 Close console
```

### Running a Decoy Scan

1. **Select operation** — Choose `[01] DECOY SCAN`
2. **Enter target** — Lab IP (e.g., `192.168.1.100`) or domain
3. **Choose decoys** — Select 1–10 nodes (default: 3)
4. **Port range** — Pick preset or enter custom (default: 1-200)
5. **Verbose mode** — Enable telemetry output (default: ON)
6. **Authorization** — Confirm you own/are authorized for this network
7. **Execute** — Watch the scan in real-time
8. **Results** — View open ports, services, scan duration
9. **Report** — Auto-saved to `~/decoy_reports/scan_TIMESTAMP.txt`

### Example Session

```bash
$ sudo python3 decoy_lab.py

[Boot sequence…]

SELECT OPERATION: 01

TARGET ──► 192.168.1.50

DECOY MATRIX:
  Select: 05

PORT MATRIX:
  PORTS ──► 1-200

VERBOSE MODE:
  [ ON ]  ◉ ACTIVE (default)

AUTHORIZATION GATE:
  CONFIRM ──► Y

[LIVE OPERATION]
  Target:       192.168.1.50
  Decoys:       05
  Ports:        1-200
  Verbose:      ON
  Status:       ████████░░ 85%

[Results]
  Open ports:   12
  Duration:     00:02:17
  Status:       ● SUCCESS
  Report:       ~/decoy_reports/scan_20240101_120530.txt
```

---

## How Decoys Work

Nmap's `-D RND:N` flag injects random fake source IPs into scan packets:

```
Real Attacker (you)     ──┐
                           ├──► Target sees multiple sources
Fake Decoy IP #1        ──┤    (harder to identify real scanner)
Fake Decoy IP #2        ──┤
Fake Decoy IP #3        ──┘
```

Only the real attacker's IP completes the TCP handshake, visible in Wireshark.

**Supported decoy counts:** 1–10 (limit enforced by tool)

---

## Security & Constraints

### ✅ Allowed

- Decoy scanning on authorized lab networks
- `-D RND:N` injection (random fake IPs)
- Custom port ranges (1–65535)
- Verbose output & telemetry
- Report generation
- Multiple scans

### ❌ Blocked

- Arbitrary `-S` source spoofing (IP must be real or decoy mode)
- Exploit automation or payload delivery
- Scanning networks you don't own/aren't authorized for
- Decoy count > 10
- Anonymous attack mode

**This tool is for authorized security labs only.** Unauthorized port scanning may be illegal in your jurisdiction.

---

## File Structure

```
Nmap_DecoyScan/
├── decoy_lab.py              # Main application (Python)
├── requirements.txt           # Dependencies (rich)
├── KALI_INSTALL_GUIDE.md     # Detailed installation guide
├── README.md                  # This file
└── LICENSE                    # Educational use license
```

---

## Installation Troubleshooting

### "nmap: command not found"
```bash
sudo apt update && sudo apt install nmap -y
```

### "ModuleNotFoundError: No module named 'rich'"
```bash
pip3 install --break-system-packages rich
```

### "Permission denied" when running
```bash
sudo python3 decoy_lab.py
# or
sudo chmod +x decoy_lab.py
```

### Scan hangs or times out
- Reduce port range: `1-100` instead of `1-65535`
- Use fewer decoys: `1-3` instead of `10`
- Check connectivity: `ping <target>`
- Verify target is in your lab network

---

## System Requirements

| Component      | Requirement          | Status |
|---|---|---|
| OS             | Kali Linux / Parrot  | ✅ Tested |
| Architecture   | x86_64 or ARM64      | ✅ Supported |
| Python         | 3.7+                 | ✅ Required |
| Nmap           | 7.80+                | ✅ Required |
| Rich Library   | 13.0+                | ✅ Auto-installed |
| RAM            | 256MB+               | ✅ Minimal |
| Root/Sudo      | Required             | ✅ For raw sockets |

---

## Reports

Scan reports are automatically saved to:

```
~/decoy_reports/scan_YYYYMMDD_HHMMSS.txt
```

Each report contains:
- Target IP & timestamp
- Decoy count & port range
- List of open ports + services
- Raw nmap output
- Scan duration

---

## Advanced Usage

### Custom Port Ranges

```
Standard presets:
  1-200      (default, common services)
  1-1024     (well-known ports)
  80         (HTTP only)
  22,80,443  (SSH, HTTP, HTTPS)
  1-65535    (all ports, slower)

Custom:
  Just type any nmap-valid range (e.g., "8000-9000")
```

### Adjusting Decoy Count

```
Default: 3 decoys
Min:     1 decoy
Max:     10 decoys

Higher = more obfuscation, slightly slower scan
Lower = faster, but easier to identify
```

### Verbose Output

When enabled, shows real-time nmap telemetry:
```
[●] Initializing scanner
[✓] Target validated
[✓] Configuration loaded
[●] Running authorized lab scan
```

---

## Contributing

Found a bug or have a feature request? Open an issue or pull request!

---

## License

**Educational/Lab Use Only**  
Designed for authorized security research in controlled environments.  
Unauthorized port scanning may be illegal in your jurisdiction.

See `LICENSE` file for details.

---

## Credits

**Created by:** Rax Ontto  
**Terminal Framework:** Rich (Python)  
**Security Tool:** Nmap  
**Platforms:** Kali Linux, Parrot OS (Debian-based)

---

## Disclaimer

⚠️ **AUTHORIZED SECURITY LAB ONLY**

This tool is designed for:
- Authorized penetration testing
- Security research labs
- Network administrators testing their own infrastructure
- Educational cybersecurity courses

**DO NOT use for:**
- Unauthorized network scanning
- Attacking systems you don't own
- Evading security monitoring
- Any illegal activity

Users are solely responsible for compliance with applicable laws and regulations.

---

**Stay safe. Stay authorized. Happy scanning.** 🔥

---

## Quick Links

- 📖 [Detailed Installation Guide](./KALI_INSTALL_GUIDE.md)
- 🔗 [Nmap Documentation](https://nmap.org)
- 🎨 [Rich Library Docs](https://rich.readthedocs.io)
- 🐧 [Kali Linux](https://www.kali.org)
