# Git Archive Strategy - CRITICAL NON-NEGOTIABLE REQUIREMENT

> 🚨 **CRITICAL**: This branching strategy is MANDATORY for ALL commits to protect work and maintain version history.

## Overview

This repository uses a strict archive-first branching strategy to ensure NO WORK IS EVER LOST and all changes are permanently preserved on GitHub.

## 🔴 MANDATORY Git Workflow

### Every Single Commit MUST Follow This Pattern:

```bash
# 1. ALWAYS create archive branch first (NEVER skip this)
DATETIME=$(date +"%Y%m%d-%H%M%S")
BRANCH_NAME="archive/${DATETIME}-brief-commit-description"
git checkout -b "$BRANCH_NAME"

# 2. Stage and commit changes
git add .
git commit -m "Detailed commit message

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 3. Push archive branch (PERMANENT STORAGE)
git push -u origin "$BRANCH_NAME"

# 4. Merge to main
git checkout main
git merge "$BRANCH_NAME" --no-ff
git push origin main
```

## Branch Naming Convention

**Format**: `archive/YYYYMMDD-HHMMSS-brief-description`

**Examples**:
- `archive/20250915-194049-poetry-to-uv-migration-python313`
- `archive/20250915-195030-fix-circular-imports`
- `archive/20250915-200145-add-validation-scripts`
- `archive/20250915-201520-update-documentation`

## 🚨 CRITICAL RULES

### ✅ ALWAYS DO:
1. **Create archive branch FIRST** - before any commits
2. **Use datetime in branch name** - for unique identification
3. **Push archive branch** - for permanent GitHub storage
4. **NEVER delete archive branches** - they are permanent history
5. **Use descriptive commit messages** - for future reference
6. **Include Claude Code attribution** - in commit messages

### ❌ NEVER DO:
1. **Commit directly to main** - always use archive branches
2. **Delete archive branches** - they are permanent records
3. **Rebase or force push** - preserve all history
4. **Skip archive branch creation** - every commit needs archival

## Implementation Scripts

### Quick Archive Script
```bash
#!/bin/bash
# scripts/git_archive.sh
DATETIME=$(date +"%Y%m%d-%H%M%S")
DESCRIPTION="$1"
if [ -z "$DESCRIPTION" ]; then
    echo "Usage: ./scripts/git_archive.sh 'brief-description'"
    exit 1
fi

BRANCH_NAME="archive/${DATETIME}-${DESCRIPTION}"
echo "Creating archive branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"
```

### Complete Archive and Push Script
```bash
#!/bin/bash
# scripts/git_archive_push.sh
DATETIME=$(date +"%Y%m%d-%H%M%S")
DESCRIPTION="$1"
COMMIT_MSG="$2"

if [ -z "$DESCRIPTION" ] || [ -z "$COMMIT_MSG" ]; then
    echo "Usage: ./scripts/git_archive_push.sh 'brief-description' 'Detailed commit message'"
    exit 1
fi

BRANCH_NAME="archive/${DATETIME}-${DESCRIPTION}"
echo "🔄 Creating archive branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"

echo "📝 Staging changes..."
git add .

echo "💾 Committing changes..."
git commit -m "${COMMIT_MSG}

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

echo "📤 Pushing archive branch..."
git push -u origin "$BRANCH_NAME"

echo "🔄 Merging to main..."
git checkout main
git merge "$BRANCH_NAME" --no-ff

echo "📤 Pushing main..."
git push origin main

echo "✅ Archive complete: $BRANCH_NAME"
```

## Why This Strategy is Critical

### 1. **Work Protection**
- Every commit is preserved forever on GitHub
- No risk of losing changes during rebases or conflicts
- Complete audit trail of all development

### 2. **Fork Safety**
- Archive branches survive upstream merges
- Easy to revert to any previous state
- Protection against accidental overwrites

### 3. **Collaboration**
- Clear history of what changed when
- Easy to identify specific features/fixes
- Enables safe parallel development

### 4. **Migration Safety**
- Critical during Poetry→uv migration
- Preserves working states at each step
- Enables rollback if issues arise

## Archive Branch Management

### Viewing Archive Branches
```bash
# List all archive branches
git branch -r | grep archive

# Show archive branch history
git log --oneline --graph --all | grep archive
```

### Finding Specific Archives
```bash
# Find branches by date
git branch -r | grep "archive/20250915"

# Find branches by description
git branch -r | grep "migration"
```

### Archive Cleanup (NEVER DELETE)
**Rule**: Archive branches are NEVER deleted. They are permanent historical records.

If GitHub storage becomes a concern:
1. Create separate archive repository
2. Mirror archive branches there
3. Keep all branches in both locations

## Integration with Development Tools

### Pre-commit Hook
```bash
#!/bin/sh
# .git/hooks/pre-commit
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" = "main" ]; then
    echo "❌ Direct commits to main are not allowed!"
    echo "Use: ./scripts/git_archive.sh 'description'"
    exit 1
fi
```

### Makefile Integration
```makefile
.PHONY: archive
archive:
ifndef DESC
	@echo "Usage: make archive DESC='brief-description' MSG='commit message'"
	@exit 1
endif
ifndef MSG
	@echo "Usage: make archive DESC='brief-description' MSG='commit message'"
	@exit 1
endif
	@./scripts/git_archive_push.sh "$(DESC)" "$(MSG)"
```

## Emergency Procedures

### If Committed to Main by Accident
```bash
# 1. Create archive branch from current main
DATETIME=$(date +"%Y%m%d-%H%M%S")
git checkout -b "archive/${DATETIME}-emergency-main-commit"
git push -u origin "archive/${DATETIME}-emergency-main-commit"

# 2. Continue normal workflow from archive branch
```

### If Archive Branch Lost Locally
```bash
# Archive branches are on GitHub - fetch them
git fetch origin
git checkout -b local-branch-name origin/archive/YYYYMMDD-HHMMSS-description
```

## Compliance Verification

Every repository MUST have:
- [ ] Archive branches for all major changes
- [ ] No direct commits to main (without archive)
- [ ] Complete commit history preserved
- [ ] Archive branch naming follows convention
- [ ] All archive branches pushed to GitHub

**Remember**: This strategy is NOT optional. It's a critical requirement to protect all development work and maintain complete version history.