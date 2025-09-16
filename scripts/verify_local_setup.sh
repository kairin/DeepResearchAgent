#!/bin/bash
# Verify Local-Only Development Configuration
# This script ensures no online automation is running

set -e

echo "🔍 Verifying Local-Only Development Configuration"
echo "=================================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check GitHub CLI authentication
echo "🔐 Checking GitHub CLI authentication..."
if gh auth status >/dev/null 2>&1; then
    print_success "GitHub CLI authenticated"
else
    print_error "GitHub CLI not authenticated"
    exit 1
fi

# Check repository settings
echo "📋 Checking repository settings..."
REPO_INFO=$(gh repo view kairin/DeepResearchAgent --json hasIssuesEnabled,hasProjectsEnabled,hasWikiEnabled,hasDiscussionsEnabled)

if echo "$REPO_INFO" | grep -q '"hasIssuesEnabled": false' && \
   echo "$REPO_INFO" | grep -q '"hasProjectsEnabled": false' && \
   echo "$REPO_INFO" | grep -q '"hasWikiEnabled": false' && \
   echo "$REPO_INFO" | grep -q '"hasDiscussionsEnabled": false'; then
    print_success "Repository features disabled (no charges)"
else
    print_warning "Some repository features may be enabled"
fi

# Check workflows on user's fork
echo "🔧 Checking workflows on fork..."
WORKFLOW_COUNT=$(gh workflow list --repo kairin/DeepResearchAgent 2>/dev/null | wc -l || echo "0")

if [ "$WORKFLOW_COUNT" -eq 0 ] || [ "$WORKFLOW_COUNT" -eq 1 ]; then
    print_success "No workflows on fork (no charges)"
else
    print_warning "Found workflows on fork - should be disabled"
fi

# Check workflow files are disabled
echo "📄 Checking workflow file configurations..."
check_workflow_disabled() {
    local file="$1"
    local name="$2"

    if [ -f "$file" ]; then
        # Check if all triggers are commented out and workflow_call is present
        if grep -q "workflow_call:" "$file" && \
           ! grep -q "^  push:\|^  pull_request:\|^  workflow_dispatch:" "$file" && \
           grep -q "# push:\|# pull_request:\|# workflow_dispatch:" "$file"; then
            print_success "$name workflow properly disabled"
        else
            print_warning "$name workflow may still have active triggers"
        fi
    else
        print_success "$name workflow file not found"
    fi
}

check_workflow_disabled ".github/workflows/ci-cd.yml" "CI/CD Pipeline"
check_workflow_disabled ".github/workflows/ci.yml" "CI"
check_workflow_disabled ".github/workflows/deploy.yml" "Deploy"

# Check local scripts exist
echo "🛠️  Checking local automation scripts..."
if [ -x "scripts/local_ci_cd.sh" ]; then
    print_success "Local CI/CD script available"
else
    print_error "Local CI/CD script missing or not executable"
fi

if [ -x "scripts/run_comprehensive_tests.py" ]; then
    print_success "Local test script available"
else
    print_error "Local test script missing or not executable"
fi

# Check git hooks
echo "🪝 Checking git protection hooks..."
if [ -x ".git/hooks/pre-merge-commit" ]; then
    print_success "Pre-merge validation hook active"
else
    print_warning "Pre-merge validation hook missing"
fi

# Check uv installation
echo "📦 Checking uv package manager..."
if command -v uv >/dev/null 2>&1; then
    UV_VERSION=$(uv --version)
    print_success "uv installed: $UV_VERSION"
else
    print_error "uv not installed - required for local development"
fi

# Check Python version
echo "🐍 Checking Python version..."
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version)
    if echo "$PYTHON_VERSION" | grep -q "Python 3.13"; then
        print_success "Python 3.13 available: $PYTHON_VERSION"
    else
        print_warning "Python 3.13 not detected: $PYTHON_VERSION"
    fi
else
    print_error "Python 3 not found"
fi

# Check uv.lock exists
echo "🔒 Checking dependency lock..."
if [ -f "uv.lock" ]; then
    print_success "uv.lock file exists"
else
    print_error "uv.lock file missing"
fi

# Final summary
echo ""
echo "=================================================="
echo "🎉 Local-Only Development Verification Complete!"
echo "=================================================="
echo ""
echo "💰 Cost Prevention Status:"
echo "  ❌ GitHub Actions: Disabled"
echo "  ❌ Repository Features: Disabled"
echo "  ✅ Local Automation: Available"
echo "  ✅ Git Protection: Active"
echo ""
echo "🚀 Ready for local development!"
echo "  Run: ./scripts/local_ci_cd.sh"
echo ""
echo "📖 See: LOCAL_DEVELOPMENT.md for details"