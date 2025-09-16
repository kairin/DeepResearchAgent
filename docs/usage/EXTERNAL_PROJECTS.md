# Using DeepResearchAgent on External Projects

## Overview

DeepResearchAgent is designed as a **standalone research tool** that can be used across multiple projects without installation in each project directory. This approach provides clean separation, easier maintenance, and maximum flexibility.

## 🎯 Recommended Usage Pattern

### Directory Structure
```
~/Apps/
├── DeepResearchAgent/     # Research tool (keep separate)
│   ├── configs/
│   ├── src/
│   └── docs/
└── MyProject/            # Your project
    ├── src/
    ├── data/
    └── research.sh       # Optional wrapper script
```

### Basic Usage

```bash
# Always run from DeepResearchAgent directory
cd ~/Apps/DeepResearchAgent

# Analyze any external project
uv run python main.py --task "Analyze the codebase in ~/Apps/MyProject"

# Use specific configurations
uv run python main.py --config configs/config_my_project.py \
    --task "Research performance issues in ~/Apps/MyProject"
```

## 🛠️ Setup for External Projects

### Step 1: Create Project-Specific Configuration

```bash
cd ~/Apps/DeepResearchAgent

# Copy base config for your project
cp configs/config_cli_fallback.py configs/config_monthly_kyocera.py

# Edit config for project-specific settings
# configs/config_monthly_kyocera.py
```

### Step 2: Create Wrapper Script (Optional)

```bash
# In your project directory
cd ~/Apps/MonthlyKyocera

# Create wrapper script
cat > research.sh << 'EOF'
#!/bin/bash
cd ~/Apps/DeepResearchAgent
uv run python main.py --config configs/config_monthly_kyocera.py --task "$*"
EOF

chmod +x research.sh

# Now you can run from project directory
./research.sh "Analyze device performance trends"
```

## 📋 Example Use Cases

### Codebase Analysis
```bash
uv run python main.py --task "Analyze the Python codebase in ~/projects/my_app and identify potential improvements"
```

### Data Research
```bash
uv run python main.py --task "Research patterns in the CSV data files located in ~/data_sets/project_x"
```

### Documentation Review
```bash
uv run python main.py --task "Review and summarize the documentation in ~/projects/docs_project"
```

### Multi-Project Research
```bash
# Compare multiple projects
uv run python main.py --task "Compare the architectures of ~/project_a and ~/project_b"
```

## ⚙️ Configuration Management

### Project-Specific Configs

Create separate config files for different projects:

```bash
# configs/config_web_project.py - For web development projects
# configs/config_data_science.py - For data science projects
# configs/config_research.py - For research projects
```

### Environment Variables

Use different `.env` files for different contexts:

```bash
# .env.default - Default settings
# .env.research - Research-focused API keys
# .env.development - Development environment
```

## 🚀 Advanced Usage

### Batch Processing

```bash
# Create a batch file with multiple research tasks
cat > monthly_kyocera_tasks.txt << EOF
Analyze device error patterns
Generate maintenance recommendations
Research performance optimization opportunities
Validate data integrity across all sources
EOF

# Process batch tasks
while read task; do
    uv run python main.py --task "$task"
done < monthly_kyocera_tasks.txt
```

### Integration with Project Workflows

```bash
# Add to Makefile
research:
    cd ~/Apps/DeepResearchAgent && \
    uv run python main.py --config configs/config_$(PROJECT).py --task "$(TASK)"

# Usage: make research PROJECT=myproject TASK="analyze codebase"
```

## ✅ Benefits

- **🔄 Reusability**: Single installation for unlimited projects
- **📁 Clean Separation**: Research tool independent of project code
- **🔄 Easy Updates**: Update DeepResearchAgent without affecting projects
- **🎯 Focused Tool**: DeepResearchAgent remains a specialized research instrument
- **📊 Resource Efficiency**: No duplicate installations
- **🔍 Version Control**: Separate git histories for clean tracking

## 🔧 Troubleshooting

### Path Issues
```bash
# Use absolute paths to avoid confusion
uv run python main.py --task "Analyze /full/path/to/project"

# Or set working directory explicitly
cd /full/path/to/project
/path/to/DeepResearchAgent/main.py --task "Analyze current directory"
```

### Configuration Conflicts
```bash
# Use unique config names for each project
ls configs/config_*.py  # Check existing configs

# Create new config for new project
cp configs/config_cli_fallback.py configs/config_new_project.py
```

### Permission Issues
```bash
# Ensure proper permissions on wrapper scripts
chmod +x ~/project/research.sh

# Check DeepResearchAgent directory permissions
ls -la ~/Apps/DeepResearchAgent
```

## 📚 Related Documentation

- [Quick Start Guide](QUICK_START.md) - Basic usage instructions
- [Configuration Guide](../models/CONFIGURATION.md) - Detailed configuration options
- [Architecture Overview](../architecture/OVERVIEW.md) - System architecture details