#!/usr/bin/env bash
#
# Test the validator locally without Docker (faster for development)
#
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Testing Skill Doctor Locally (Python) ===${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
  echo -e "${RED}❌ Error: Must run from project root${NC}"
  exit 1
fi

# Ensure virtual environment exists
if [ ! -d ".venv" ]; then
  echo -e "${YELLOW}Creating virtual environment...${NC}"
  uv sync --all-extras
fi

# Test valid skill
echo -e "${YELLOW}✅ Testing valid skill...${NC}"
if uv run python -m skill_doctor.main \
  --path=tests/fixtures/valid-skill \
  --mode=single; then
  echo -e "${GREEN}✅ Valid skill test passed${NC}\n"
else
  echo -e "${RED}❌ Valid skill test failed${NC}\n"
  exit 1
fi

# Test invalid skill
echo -e "${YELLOW}❌ Testing invalid skill (expect errors)...${NC}"
if uv run python -m skill_doctor.main \
  --path=tests/fixtures/invalid-skill \
  --mode=single \
  --fail-on-error=false; then
  echo -e "${GREEN}✅ Invalid skill test completed${NC}\n"
else
  echo -e "${RED}❌ Invalid skill test failed unexpectedly${NC}\n"
  exit 1
fi

# Test multiple skills
echo -e "${YELLOW}📊 Testing multiple valid skills...${NC}"
if uv run python -m skill_doctor.main \
  --path="tests/fixtures/multiple-skills/all-valid/*" \
  --mode=multiple; then
  echo -e "${GREEN}✅ Multiple skills test passed${NC}\n"
else
  echo -e "${RED}❌ Multiple skills test failed${NC}\n"
  exit 1
fi

# Test edge cases
echo -e "${YELLOW}🔍 Testing edge cases...${NC}"
for test_case in name-too-long name-with-consecutive-hyphens name-with-uppercase; do
  if uv run python -m skill_doctor.main \
    --path="tests/fixtures/edge-cases/$test_case" \
    --mode=single \
    --fail-on-error=false >/dev/null 2>&1; then
    echo -e "${GREEN}  ✅ Edge case: $test_case${NC}"
  else
    echo -e "${YELLOW}  ⚠️  Edge case: $test_case (expected validation errors)${NC}"
  fi
done
echo ""

echo -e "${GREEN}🎉 All Python tests completed!${NC}"
