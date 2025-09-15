# 📚 DeepResearchAgent Documentation Index

This directory contains organized documentation for the DeepResearchAgent fork with Guardian Agents integration.

## 📁 Documentation Structure

### 🏗️ **Integration Documentation** (`integration/`)
- **[INTEGRATION_ROADMAP.md](integration/INTEGRATION_ROADMAP.md)** - Comprehensive Guardian Agents integration strategy
  - 14-week phased implementation plan
  - Complete agent mapping and categorization
  - Technical architecture and risk management
  - Success metrics and KPIs framework

### 🛠️ **Development Documentation** (`development/`)
- **[GIT_STRATEGY.md](development/GIT_STRATEGY.md)** - Mandatory git workflow and protection strategy
  - Archive-first branching strategy
  - Non-negotiable commit and push procedures
  - Branch naming conventions with datetime stamps
  - Work protection mechanisms

### 🔧 **Management Documentation** (`management/`)
- **[FORK_MANAGEMENT.md](management/FORK_MANAGEMENT.md)** - Fork maintenance and upstream sync strategies
  - Git protection mechanisms via `.gitattributes`
  - Conflict resolution guidelines
  - Critical file identification
  - Sync procedures to prevent work loss

### 🎨 **Assets** (`assets/`)
- **[integration_workflow.svg](assets/integration_workflow.svg)** - Animated workflow diagram showing transformation
- **[python_interpreter_sandbox.md](assets/python_interpreter_sandbox.md)** - Python execution environment documentation
- Various project images and visual assets

## 🚀 **Quick Navigation**

### **For New Contributors**
1. Start with [../README.md](../README.md) - Main project overview
2. Review [integration/INTEGRATION_ROADMAP.md](integration/INTEGRATION_ROADMAP.md) - Integration strategy
3. **MUST READ**: [development/GIT_STRATEGY.md](development/GIT_STRATEGY.md) - Git workflow requirements

### **For Fork Maintainers**
1. [management/FORK_MANAGEMENT.md](management/FORK_MANAGEMENT.md) - Sync strategies
2. [../CHANGELOG.md](../CHANGELOG.md) - Migration history
3. [development/GIT_STRATEGY.md](development/GIT_STRATEGY.md) - Protection mechanisms

### **For Integration Development**
1. [integration/INTEGRATION_ROADMAP.md](integration/INTEGRATION_ROADMAP.md) - Complete implementation plan
2. [assets/integration_workflow.svg](assets/integration_workflow.svg) - Visual workflow
3. [../AGENTS.md](../AGENTS.md) - Current agent documentation

## 📋 **Document Relationships**

```
README.md (Root)
├── Links to: docs/integration/INTEGRATION_ROADMAP.md
├── Links to: docs/management/FORK_MANAGEMENT.md
└── References: CHANGELOG.md

AGENTS.md (Root)
└── Links to: docs/development/GIT_STRATEGY.md

docs/integration/INTEGRATION_ROADMAP.md
├── Links to: ../management/FORK_MANAGEMENT.md
└── Links to: ../../CHANGELOG.md

docs/management/FORK_MANAGEMENT.md
└── Self-references updated paths

docs/development/GIT_STRATEGY.md
└── Standalone strategy document
```

## 🔄 **Maintenance Notes**

- All documentation paths have been updated to reflect the new structure
- Relative links are used to maintain portability
- The main README.md serves as the primary entry point
- This DOCUMENTATION_INDEX.md serves as a navigation hub for detailed documentation

---

**📍 Current Location**: `/docs/DOCUMENTATION_INDEX.md`
**🔗 Navigation**: [← Back to Main README](../README.md) | [Integration Roadmap →](integration/INTEGRATION_ROADMAP.md)