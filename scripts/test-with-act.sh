#!/usr/bin/env bash
#
# Run GitHub Actions workflows locally with Act
#
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if act is installed
if ! command -v act &> /dev/null; then
  echo -e "${RED}❌ Act is not installed${NC}"
  echo ""
  echo "Install with:"
  echo "  macOS:   brew install act"
  echo "  Linux:   curl https://raw.githubusercontent.com/nektos/act/master/install.sh | bash"
  echo "  Windows: choco install act-cli"
  echo ""
  echo "Learn more: https://github.com/nektos/act"
  exit 1
fi

# Parse arguments
JOB="${1:-test-action}"
WORKFLOW="${2:-.github/workflows/ci.yml}"

echo -e "${YELLOW}🎬 Running workflow with Act${NC}"
echo -e "  Workflow: ${WORKFLOW}"
echo -e "  Job: ${JOB}"
echo ""

# Run act
echo -e "${YELLOW}Starting Act...${NC}"
act -j "$JOB" -W "$WORKFLOW"

if [ $? -eq 0 ]; then
  echo ""
  echo -e "${GREEN}✅ Workflow completed successfully${NC}"
else
  echo ""
  echo -e "${RED}❌ Workflow failed${NC}"
  exit 1
fi
