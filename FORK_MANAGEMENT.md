# Fork Management Strategy

This document outlines strategies to protect your fork-specific changes when syncing with the original DeepResearchAgent repository.

## Overview

This fork has undergone significant changes, particularly the migration from Poetry to uv and upgrade to Python 3.13. These changes are substantial and may conflict with upstream updates.

## Critical Fork-Specific Files

### 🔴 High Risk - Major Modifications (Likely to Conflict)

These files have been significantly modified and will likely conflict with upstream changes:

| File | Type | Description | Risk Level |
|------|------|-------------|-----------|
| `pyproject.toml` | Build Config | Migrated from Poetry to uv format | **CRITICAL** |
| `Makefile` | Build Scripts | All commands converted to uv | **HIGH** |
| `uv.lock` | Dependencies | uv-specific lock file | **MEDIUM** |

### 🟡 Medium Risk - Moderate Modifications

| File | Type | Description | Risk Level |
|------|------|-------------|-----------|
| `README.md` | Documentation | Updated installation instructions | **MEDIUM** |
| `AGENTS.md` | Documentation | Updated with uv commands | **MEDIUM** |
| `src/tools/*.py` | Source Code | Fixed circular imports | **MEDIUM** |
| `src/utils/agent_types.py` | Source Code | Fixed circular import | **LOW** |
| `src/tools/markdown/mdconvert.py` | Source Code | markitdown API fixes | **MEDIUM** |
| `src/utils/url_utils.py` | Source Code | markitdown import fix | **LOW** |
| `src/tools/web_fetcher.py` | Source Code | markitdown import fix | **LOW** |

### 🟢 Fork-Specific Files (Safe)

These files are specific to your fork and won't conflict:

| File | Description |
|------|-------------|
| `CHANGELOG.md` | Migration documentation |
| `FORK_MANAGEMENT.md` | This file |
| `scripts/validate_migration.py` | Validation script |
| `migration_validation_report.json` | Validation results |

## Sync Strategies

### Strategy 1: Protected Branch Approach (Recommended)

1. **Create a protected branch for your changes:**
   ```bash
   git checkout -b fork-uv-migration
   git push -u origin fork-uv-migration
   ```

2. **Keep main branch for upstream sync:**
   ```bash
   git checkout main
   git remote add upstream https://github.com/SkyworkAI/DeepResearchAgent.git
   git fetch upstream
   git merge upstream/main
   ```

3. **Merge upstream changes selectively:**
   ```bash
   git checkout fork-uv-migration
   git merge main --no-commit --no-ff
   # Resolve conflicts manually
   # Validate with: uv run python scripts/validate_migration.py
   git commit -m "Merge upstream changes, maintain uv migration"
   ```

### Strategy 2: File-Level Protection

1. **Use git attributes to handle merge conflicts:**
   ```bash
   echo "pyproject.toml merge=ours" >> .gitattributes
   echo "Makefile merge=ours" >> .gitattributes
   echo "uv.lock merge=ours" >> .gitattributes
   ```

2. **Configure merge driver:**
   ```bash
   git config merge.ours.driver true
   ```

### Strategy 3: Cherry-Pick Approach

1. **Don't merge directly, cherry-pick specific commits:**
   ```bash
   git remote add upstream https://github.com/SkyworkAI/DeepResearchAgent.git
   git fetch upstream
   git log upstream/main --oneline
   git cherry-pick <commit-hash>  # Pick specific changes
   ```

## Pre-Sync Checklist

Before syncing with upstream, always:

- [ ] Run validation: `uv run python scripts/validate_migration.py`
- [ ] Backup your changes: `git stash push -u -m "Pre-sync backup"`
- [ ] Document current state: `git log --oneline -10 > pre-sync-state.txt`
- [ ] Create a backup branch: `git checkout -b backup-$(date +%Y%m%d)`

## Post-Sync Validation

After any merge or sync:

1. **Validate migration integrity:**
   ```bash
   uv run python scripts/validate_migration.py
   ```

2. **Test core functionality:**
   ```bash
   make clean && make venv-system && make install
   uv run python -c "import src; print('Import test passed')"
   ```

3. **Run integration tests:**
   ```bash
   uv run pytest tests/ -v
   ```

## Conflict Resolution Guidelines

### pyproject.toml Conflicts

**Always keep your version** - the migration to uv format is fundamental:

```toml
# Keep these sections:
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
dependencies = [
    # Your uv-format dependencies
]

[tool.uv]
dev-dependencies = [
    # Your dev dependencies
]
```

### Makefile Conflicts

**Keep your uv commands** but integrate new targets:

```makefile
# Keep your uv-based commands:
install:
    uv sync --all-extras

# But add new upstream targets with uv conversion
```

### Source Code Conflicts

For Python files, carefully review each conflict:

1. **Import fixes**: Keep your circular import fixes
2. **API updates**: Keep markitdown API fixes
3. **New features**: Integrate upstream features carefully
4. **Dependencies**: Ensure new deps are added via `uv add`

## Automated Validation

Set up a pre-commit hook to validate changes:

```bash
#!/bin/sh
# .git/hooks/pre-commit
echo "Validating migration integrity..."
uv run python scripts/validate_migration.py || exit 1
```

## Documentation Sync

When upstream changes documentation:

1. **README.md**: Merge content but keep uv installation instructions
2. **AGENTS.md**: Keep your uv-specific updates
3. **New docs**: Convert any Poetry references to uv equivalents

## Emergency Recovery

If a sync breaks your migration:

1. **Restore from backup:**
   ```bash
   git reset --hard backup-<date>
   ```

2. **Re-validate:**
   ```bash
   uv run python scripts/validate_migration.py
   ```

3. **Re-apply critical fixes:**
   - Check import fixes in `src/tools/`
   - Verify markitdown fixes
   - Ensure uv configuration

## Best Practices

1. **Frequent small syncs** are better than large infrequent ones
2. **Always validate** after any merge
3. **Document conflicts** and resolutions in commit messages
4. **Maintain your test suite** to catch regressions
5. **Keep migration documentation updated**

## Communication

When contributing back to upstream:

1. **Separate PRs** for different types of changes
2. **Document uv benefits** if proposing migration upstream
3. **Provide migration tools** like your validation script
4. **Maintain compatibility** during transition periods

## Monitoring Upstream

Set up notifications for upstream changes:

```bash
# Watch for changes in critical files
git remote add upstream https://github.com/SkyworkAI/DeepResearchAgent.git
git fetch upstream
git diff upstream/main -- pyproject.toml Makefile README.md
```

## Support

If you encounter issues:

1. Run the validation script for detailed diagnostics
2. Check the migration report JSON for specific failures
3. Consult the CHANGELOG.md for known compatibility issues
4. Test in a clean environment before applying fixes

Remember: Your migration to uv and Python 3.13 provides significant benefits (faster dependency resolution, modern Python features, better tooling). The protection strategies ensure you maintain these benefits while staying current with upstream improvements.