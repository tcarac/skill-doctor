#!/usr/bin/env bash
#
# Test Docker build and basic functionality locally
#
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Skill Doctor Docker Test Suite ===${NC}\n"

# Build the image
echo -e "${YELLOW}📦 Building Docker image...${NC}"
docker build -t skill-doctor:test .
echo -e "${GREEN}✅ Docker build successful${NC}\n"

# Test help command
echo -e "${YELLOW}📖 Testing --help command...${NC}"
if docker run --rm skill-doctor:test --help > /dev/null 2>&1; then
  echo -e "${GREEN}✅ Help command works${NC}\n"
else
  echo -e "${RED}❌ Help command failed${NC}\n"
  exit 1
fi

# Test with valid skill
echo -e "${YELLOW}✅ Testing with valid skill...${NC}"
if docker run --rm \
  -v "$(pwd)/tests/fixtures:/workspace" \
  skill-doctor:test \
  --path=/workspace/valid-skill \
  --mode=single; then
  echo -e "${GREEN}✅ Valid skill test passed${NC}\n"
else
  echo -e "${RED}❌ Valid skill test failed${NC}\n"
  exit 1
fi

# Test with invalid skill (should fail)
echo -e "${YELLOW}❌ Testing with invalid skill (expect failure)...${NC}"
if docker run --rm \
  -v "$(pwd)/tests/fixtures:/workspace" \
  skill-doctor:test \
  --path=/workspace/invalid-skill \
  --mode=single 2>&1 | grep -q "Failed: 1"; then
  echo -e "${GREEN}✅ Invalid skill test passed (correctly failed)${NC}\n"
else
  echo -e "${RED}❌ Invalid skill test did not fail as expected${NC}\n"
  exit 1
fi

# Test multiple skills
echo -e "${YELLOW}📊 Testing multiple skills...${NC}"
if docker run --rm \
  -v "$(pwd)/tests/fixtures:/workspace" \
  skill-doctor:test \
  --path="/workspace/multiple-skills/all-valid/*" \
  --mode=multiple; then
  echo -e "${GREEN}✅ Multiple skills test passed${NC}\n"
else
  echo -e "${RED}❌ Multiple skills test failed${NC}\n"
  exit 1
fi

# Test edge case - name too long
echo -e "${YELLOW}🔍 Testing edge case (name too long)...${NC}"
if docker run --rm \
  -v "$(pwd)/tests/fixtures:/workspace" \
  skill-doctor:test \
  --path=/workspace/edge-cases/name-too-long \
  --mode=single 2>&1 | grep -q "Failed: 1"; then
  echo -e "${GREEN}✅ Edge case test passed${NC}\n"
else
  echo -e "${RED}❌ Edge case test failed${NC}\n"
  exit 1
fi

echo -e "${GREEN}🎉 All Docker tests passed!${NC}"
