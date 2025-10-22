#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running LegalFlow AI Test Suite${NC}\n"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests
echo -e "${YELLOW}Running pytest...${NC}"
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

# Check exit code
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✓ All tests passed!${NC}"
    echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
else
    echo -e "\n${RED}✗ Some tests failed${NC}"
    exit 1
fi

# Display coverage summary
echo -e "\n${YELLOW}Coverage Summary:${NC}"
coverage report --skip-empty

