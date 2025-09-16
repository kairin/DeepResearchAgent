# 📚 DeepResearchAgent Documentation Index

Complete documentation structure for DeepResearchAgent with organized guides and references.

## 📁 Documentation Structure

### 🚀 **Getting Started**
- **[../AGENTS.md](../AGENTS.md)** - Main project documentation (concise overview)
- **[setup/ENVIRONMENT_SETUP.md](setup/ENVIRONMENT_SETUP.md)** - Complete installation guide
- **[usage/QUICK_START.md](usage/QUICK_START.md)** - Get running in 5 minutes
- **[usage/EXTERNAL_PROJECTS.md](usage/EXTERNAL_PROJECTS.md)** - Using on external projects (recommended)
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

### 🏗️ **Architecture & Design**
- **[architecture/OVERVIEW.md](architecture/OVERVIEW.md)** - System design and components
- **[SVG_TUI_INTEGRATION.md](SVG_TUI_INTEGRATION.md)** - SVG-TUI roadmap and integration
- **[models/CONFIGURATION.md](models/CONFIGURATION.md)** - LLM provider setup guide

### 🛠️ **Development & Contributing**
- **[development/GIT_STRATEGY.md](development/GIT_STRATEGY.md)** - **MANDATORY** git workflow
- **[development/TEST_SYSTEM_IMPROVEMENTS_SUMMARY.md](development/TEST_SYSTEM_IMPROVEMENTS_SUMMARY.md)** - Test system improvements and validation fixes
- **[development/CONTRIBUTING.md](development/CONTRIBUTING.md)** - Contribution guidelines
- **[security/GUIDELINES.md](security/GUIDELINES.md)** - Security best practices
- **[standards/DOCUMENTATION_STANDARDS.md](standards/DOCUMENTATION_STANDARDS.md)** - Documentation standards

### 📋 **Project Planning** (`planning/`)
- **[planning/PROJECT_ROADMAP.md](planning/PROJECT_ROADMAP.md)** - 4-phase development plan
- **[planning/phase1/IMMEDIATE_ACTION_PLAN.md](planning/phase1/IMMEDIATE_ACTION_PLAN.md)** - Critical fixes (✅ completed)
- **[IMMEDIATE_FIXES_README.md](IMMEDIATE_FIXES_README.md)** - Phase 1 fixes summary

### 🔧 **Legacy Integration** (`integration/`, `management/`)
- **[integration/INTEGRATION_ROADMAP.md](integration/INTEGRATION_ROADMAP.md)** - Guardian Agents integration
- **[management/FORK_MANAGEMENT.md](management/FORK_MANAGEMENT.md)** - Fork maintenance strategies

## 🚀 **Quick Navigation**

### **For New Users**
1. Start with [../AGENTS.md](../AGENTS.md) - Project overview
2. Follow [usage/QUICK_START.md](usage/QUICK_START.md) - Get running quickly
3. Setup with [setup/ENVIRONMENT_SETUP.md](setup/ENVIRONMENT_SETUP.md) - Complete installation

### **For Developers**
1. **MUST READ**: [development/GIT_STRATEGY.md](development/GIT_STRATEGY.md) - Non-negotiable workflow
2. Review [development/CONTRIBUTING.md](development/CONTRIBUTING.md) - How to contribute
3. Understand [architecture/OVERVIEW.md](architecture/OVERVIEW.md) - System design

### **For Troubleshooting**
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
2. Review [IMMEDIATE_FIXES_README.md](IMMEDIATE_FIXES_README.md) - Quick fixes
3. Validate [models/CONFIGURATION.md](models/CONFIGURATION.md) - Model setup

## 📋 **Document Relationships**

```
AGENTS.md (Root - Main Entry)
├── Links to: docs/setup/ENVIRONMENT_SETUP.md
├── Links to: docs/usage/QUICK_START.md
├── Links to: docs/architecture/OVERVIEW.md
├── Links to: docs/models/CONFIGURATION.md
└── Links to: docs/development/GIT_STRATEGY.md

docs/setup/ENVIRONMENT_SETUP.md
├── Links to: ../architecture/OVERVIEW.md
├── Links to: ../models/CONFIGURATION.md
└── Links to: ../TROUBLESHOOTING.md

docs/usage/QUICK_START.md
├── Links to: ../setup/ENVIRONMENT_SETUP.md
├── Links to: ../models/CONFIGURATION.md
└── Links to: ../troubleshooting/COMMON_ISSUES.md

docs/architecture/OVERVIEW.md
├── Links to: ../development/AGENT_DEVELOPMENT.md
├── Links to: ../models/INTEGRATION.md
└── Links to: ../security/GUIDELINES.md

docs/models/CONFIGURATION.md
├── Links to: ../setup/ENVIRONMENT_SETUP.md
└── Links to: ../examples/MODEL_INTEGRATION.md
```

## 🎯 **Documentation by Use Case**

### I want to get started quickly
1. [../AGENTS.md](../AGENTS.md) → [usage/QUICK_START.md](usage/QUICK_START.md) → Run examples

### I want to understand the system
1. [architecture/OVERVIEW.md](architecture/OVERVIEW.md) → [SVG_TUI_INTEGRATION.md](SVG_TUI_INTEGRATION.md)

### I want to configure models
1. [models/CONFIGURATION.md](models/CONFIGURATION.md) → [setup/ENVIRONMENT_SETUP.md](setup/ENVIRONMENT_SETUP.md)

### I want to contribute
1. [development/GIT_STRATEGY.md](development/GIT_STRATEGY.md) → [development/CONTRIBUTING.md](development/CONTRIBUTING.md)

### I have problems
1. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) → [IMMEDIATE_FIXES_README.md](IMMEDIATE_FIXES_README.md)

## ✅ **Documentation Status**

- ✅ **AGENTS.md** - Simplified and concise with deep links
- ✅ **Environment Setup** - Complete installation guide
- ✅ **Architecture Overview** - System design documentation
- ✅ **Model Configuration** - LLM provider setup guide
- ✅ **Quick Start** - 5-minute tutorial
- ✅ **Troubleshooting** - Issue resolution guide
- ✅ **Phase 1 Implementation** - Critical fixes completed
- 🚧 **Contributing Guidelines** - In development
- 🚧 **Security Guidelines** - In development
- 📋 **Usage Examples** - Planned

## 🤝 **Contributing to Documentation**

All documentation changes must follow the [Git Strategy](development/GIT_STRATEGY.md):

```bash
DATETIME=$(date +"%Y%m%d-%H%M%S")
git checkout -b "archive/${DATETIME}-update-docs"
# Make changes
git add . && git commit -m "Update documentation"
git push -u origin "archive/${DATETIME}-update-docs"
git checkout main && git merge "archive/${DATETIME}-update-docs" --no-ff
```

---

**📍 Current Location**: `/docs/DOCUMENTATION_INDEX.md`
**🔗 Navigation**: [← Back to AGENTS.md](../AGENTS.md) | [Quick Start →](usage/QUICK_START.md)