# File Organization Guide

> 📂 **Clean Structure**: All files have been organized into proper subfolders while maintaining functionality

## 🎯 **Organization Summary**

### **Root Directory** (Ultra-Critical Emergency Tools Only)
```
/fix                 # 5-character emergency terminal cleanup script
/f.py                # Minimal Python one-liner emergency cleanup
```
**Why in root**: During terminal floods, you need ultra-fast access with minimal typing.

### **Emergency Tools** → `/tools/emergency/`
```
tools/emergency/
├── fix_mouse.py           # User-friendly mouse tracking fix
└── emergency_cleanup.py   # Auto-import cleanup module
```

### **Development Tools** → `/tools/development/`
```
tools/development/
├── debug_terminal.py      # Terminal diagnostics and debugging
├── test_minimal_tui.py    # Minimal TUI testing utility
└── test_textual.py        # Textual framework testing
```

### **Scripts** → `/scripts/`
```
scripts/
├── run_tui.sh             # TUI launcher script (moved from root)
├── resume_cleanup.sh      # Session resume cleanup
├── terminal_cleanup.py    # Terminal cleanup utility
├── local_ci_cd.sh        # Local CI/CD pipeline
└── ...                   # Other existing scripts
```

### **Development Documentation** → `/docs/development/`
```
docs/development/
├── LOCAL_DEVELOPMENT.md   # Local development guide (moved from root)
├── GIT_STRATEGY.md       # Git workflow documentation
├── CONTRIBUTING.md       # Contribution guidelines
└── ...                   # Other development docs
```

### **Backup Files** → `/backup/` (Ignored by Git)
```
backup/
├── pyproject.toml.bak     # Backup configuration files
├── requirements.txt.bak   # Backup requirements
└── ...                   # Other backup files
```

## 📝 **Updated Commands**

### **Emergency Recovery** (Updated Paths)
```bash
# Ultra-fast (still in root):
./fix
python3 f.py

# Detailed recovery:
uv run python tools/emergency/fix_mouse.py
uv run python tools/emergency/emergency_cleanup.py
```

### **Development & Testing** (Updated Paths)
```bash
# TUI testing:
uv run python tools/development/test_minimal_tui.py

# Terminal diagnostics:
uv run python tools/development/debug_terminal.py

# TUI launcher:
./scripts/run_tui.sh
```

### **Scripts** (Updated Paths)
```bash
# Local CI/CD:
./scripts/local_ci_cd.sh

# Terminal cleanup:
./scripts/resume_cleanup.sh
```

## ✅ **Functionality Verified**

All moved files have been tested and confirmed to work correctly in their new locations:

- ✅ **Emergency tools** - Mouse tracking cleanup works from `/tools/emergency/`
- ✅ **Development tools** - TUI testing and debugging work from `/tools/development/`
- ✅ **Scripts** - All scripts function correctly from `/scripts/`
- ✅ **Documentation** - All links and references updated

## 🔗 **Documentation Updates**

Updated references in:
- `/docs/TERMINAL_RECOVERY.md` - Emergency command paths
- `/docs/TROUBLESHOOTING.md` - Tool paths and debugging commands
- `/CLAUDE.md` - Quick reference commands
- `/docs/FILE_ORGANIZATION.md` - This file

## 🚫 **Ignored Files**

Added to `.gitignore`:
```gitignore
# Backup files
backup/
*.bak
```

## 🎯 **Benefits of This Organization**

### **Cleaner Root Directory**
- Only essential files (`main.py`, config files, essential scripts)
- Ultra-critical emergency tools (`fix`, `f.py`) remain easily accessible

### **Logical Grouping**
- **Emergency tools** grouped together for crisis situations
- **Development tools** organized for contributors and debugging
- **Backup files** isolated and git-ignored

### **Maintained Functionality**
- All paths updated in documentation
- All tools tested and confirmed working
- Emergency accessibility preserved

### **Better Navigation**
- Clear folder structure for new contributors
- Related tools grouped together
- Reduced clutter in root directory

## 🔄 **Migration Complete**

**Status**: ✅ All files successfully reorganized with maintained functionality

**Next Steps**:
- Commit the organized structure
- All emergency tools remain fully functional
- Development workflow improved with cleaner organization