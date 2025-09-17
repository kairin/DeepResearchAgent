# Terminal Recovery Guide

> 🚨 **Critical Documentation**: Mouse tracking escape sequences can completely flood your terminal, making it impossible to type commands. This guide provides emergency recovery solutions.

## Problem Overview

### What Happens
When the TUI (Text User Interface) exits improperly, mouse tracking remains enabled in your terminal. This causes:
- **Mouse movement floods terminal** with escape sequences like `<35;83;16M`
- **Terminal becomes completely unresponsive** - you cannot type any commands
- **Scrolling is impossible** due to continuous escape sequence output
- **Normal terminal commands fail** because input is overwhelmed

### Root Cause
1. **TUI Applications** (like our DeepResearchTUI) enable mouse tracking to capture clicks/movement
2. **Improper Exit** (crashes, force-kills, session interrupts) leaves mouse tracking enabled
3. **Terminal Sends Mouse Data** as escape sequences for every pixel of mouse movement
4. **Flood Effect** makes terminal completely unusable

## 🚨 Emergency Recovery (Terminal Completely Flooded)

### Method 1: Force Terminal Restart (Fastest)
```bash
# When you can't type anything:
# 1. Close the entire terminal window/tab (click X or Ctrl+Shift+W)
# 2. Open a new terminal window
# 3. Mouse tracking only affects the specific terminal session
```

### Method 2: Keyboard Interrupts
Try these **in rapid succession** when terminal is flooded:

```bash
# Try each of these rapidly (hold down keys):
Ctrl+C Ctrl+C Ctrl+C    # Interrupt signal (most likely to work)
Ctrl+Z                  # Suspend current process
Ctrl+\                  # Force quit signal (SIGQUIT)
Ctrl+D                  # End input/session
```

**Technique**: Hold the key combinations and press them multiple times rapidly. Sometimes you need to "break through" the flood.

### Method 3: Alternative Terminal Access
```bash
# Open another terminal while the flooded one runs:
# - New terminal window/tab in same application
# - Different terminal application entirely
# - SSH into same machine from another terminal
# - Use terminal multiplexer (tmux/screen) to create new session
```

## 🔧 Emergency Commands (When You Get Control)

### Ultra-Short Recovery Commands
Once you break through the flood or get a brief typing opportunity:

```bash
# Shortest possible - just 5 characters:
./fix

# Alternative minimal Python (9 characters):
python3 f.py

# With uv (if available):
uv run python f.py

# Manual escape sequences (if scripts don't work):
printf '\033[?1000l\033[?1002l\033[?1003l\033[?1006l\033[?1015l'
```

### Standard Recovery Commands
```bash
# Comprehensive cleanup:
uv run python tools/emergency/fix_mouse.py

# Shell script cleanup:
./scripts/resume_cleanup.sh

# Manual terminal reset:
reset && stty sane

# Emergency Python module:
uv run python tools/emergency/emergency_cleanup.py
```

## ⚡ Quick Reference Card

**Print this or keep it handy for emergencies:**

```
TERMINAL FLOODED WITH MOUSE ESCAPES:

1. Close terminal window → Open new terminal (FASTEST)

2. Rapid key press: Ctrl+C Ctrl+C Ctrl+C

3. Type quickly: ./fix

4. Last resort: Restart terminal application
```

## 🛡️ Prevention Systems

### Automatic Prevention (Already Implemented)
- **main.py Emergency Cleanup**: Mouse tracking disabled on script startup
- **TUI Exit Handlers**: Proper cleanup when quitting with 'q'
- **Signal Handlers**: Cleanup on Ctrl+C, crashes, interrupts
- **Session Resume Cleanup**: Automatic cleanup when resuming Claude Code sessions

### Manual Prevention
```bash
# Always run this after any TUI session:
uv run python fix_mouse.py

# Or include cleanup in your shell profile:
echo 'printf "\\033[?1000l\\033[?1002l\\033[?1003l"' >> ~/.bashrc
```

## 🔍 Technical Details

### Mouse Tracking Escape Sequences
These ANSI escape sequences control mouse tracking:

```bash
\033[?1000h    # Enable X11 mouse reporting
\033[?1000l    # Disable X11 mouse reporting
\033[?1002h    # Enable cell motion mouse tracking
\033[?1002l    # Disable cell motion mouse tracking
\033[?1003h    # Enable all motion mouse tracking
\033[?1003l    # Disable all motion mouse tracking
\033[?1006h    # Enable SGR mouse mode
\033[?1006l    # Disable SGR mouse mode
\033[?1015h    # Enable urxvt mouse mode
\033[?1015l    # Disable urxvt mouse mode
```

### Mouse Data Format
When enabled, mouse movement sends sequences like:
```
<35;83;16M     # Mouse move to column 83, row 16, button 35
<35;84;16M     # Mouse move to column 84, row 16, button 35
<35;85;16M     # Mouse move to column 85, row 16, button 35
```

At 60fps mouse movement, this floods hundreds of sequences per second.

### Terminal State Recovery
Complete terminal state reset sequence:
```bash
\033[?1000l    # Disable X11 mouse reporting
\033[?1002l    # Disable cell motion mouse tracking
\033[?1003l    # Disable all motion mouse tracking
\033[?1006l    # Disable SGR mouse mode
\033[?1015l    # Disable urxvt mouse mode
\033[?25h      # Show cursor
\033[?1049l    # Exit alternate screen
\033[?1004l    # Disable focus reporting
\033[?2004l    # Disable bracketed paste
\033c          # Full terminal reset
\033[0m        # Reset colors/formatting
```

## 📁 Emergency Files Created

### `/fix` - Minimal Emergency Script
```bash
#!/bin/bash
printf '\033[?1000l\033[?1002l\033[?1003l\033[?1006l\033[?1015l\033[?25h\033[?1049l\033[?1004l\033[?2004l'&&stty sane&&reset&&echo "Fixed"
```

### `/f.py` - One-Line Python Emergency
```python
import sys,os;[sys.stdout.write(s)for s in['\033[?1000l','\033[?1002l','\033[?1003l','\033[?1006l','\033[?1015l']];sys.stdout.flush();os.system('stty sane');print('Fixed')
```

### `/tools/emergency/fix_mouse.py` - User-Friendly Recovery
```python
#!/usr/bin/env python3
"""Quick fix for mouse escape sequences."""
# Comprehensive mouse tracking cleanup with user feedback
```

### `/tools/emergency/emergency_cleanup.py` - Auto-Import Recovery
```python
#!/usr/bin/env python3
"""Emergency terminal cleanup - runs automatically on import."""
# Automatic cleanup with signal handlers
```

### `/scripts/resume_cleanup.sh` - Session Resume Recovery
```bash
#!/bin/bash
# Terminal cleanup script for Claude Code session resume
# Comprehensive terminal state reset
```

## 🧪 Testing Emergency Procedures

### Simulate Mouse Flood (FOR TESTING ONLY)
```bash
# DO NOT RUN THIS unless you want to test recovery:
printf '\033[?1003h'  # Enable all mouse tracking
# Move mouse rapidly - terminal will flood with escapes
# Use recovery methods above to fix
```

### Verify Recovery Works
```bash
# After recovery, test mouse tracking is disabled:
echo "Move mouse - you should see NO escape sequences"
# If you see escape sequences, recovery failed
```

## 🔗 Related Issues

### Common Scenarios That Cause This
1. **TUI Application Crashes** during mouse-enabled mode
2. **Force-killing TUI process** with kill -9 or Task Manager
3. **Terminal Session Interruption** during TUI execution
4. **SSH Connection Drops** while running TUI remotely
5. **Claude Code Session Resume** inheriting corrupted terminal state

### Applications That Can Cause This
- **Textual-based TUIs** (like DeepResearchTUI)
- **ncurses applications** with mouse support
- **tmux/screen** with mouse mode enabled
- **vim/nvim** with mouse support
- **htop** and other interactive tools

### Prevention for Other Applications
```bash
# Add to ~/.bashrc to auto-cleanup on shell start:
printf '\033[?1000l\033[?1002l\033[?1003l\033[?1006l\033[?1015l'

# Or create alias for any risky command:
alias safe_tui='trap "printf \"\\033[?1000l\\033[?1002l\\033[?1003l\"" EXIT; your_tui_command'
```

## ⚠️ Known Limitations

### When Emergency Recovery May Fail
1. **Terminal emulator bugs** - Some terminals don't properly handle escape sequences
2. **Remote sessions** - SSH/telnet may buffer or modify escape sequences
3. **Terminal multiplexers** - tmux/screen may interfere with escape sequence handling
4. **Very old terminals** - May not support modern mouse tracking modes

### Backup Recovery Methods
1. **Kill terminal process from outside** (Task Manager, kill command from another terminal)
2. **Restart terminal emulator application** completely
3. **Log out and back in** to reset all terminal sessions
4. **Reboot system** (extreme last resort)

---

**Remember**: The fastest recovery is almost always closing the terminal window and opening a new one. Don't spend time fighting the flood - just restart the session.