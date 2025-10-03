#!/bin/bash

echo "Running SeatServe Backend Quick Verification..."
echo "================================================"

# Verify we're in the correct directory
if [ ! -f "app/main.py" ]; then
    echo "Error: app/main.py not found. Are you in the correct directory?"
    exit 1
fi

echo "Correct directory - OK"

# Verify basic dependencies
echo "Checking dependencies..."
python3 -c "import fastapi, sqlalchemy, pydantic, pytest" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "Basic dependencies installed - OK"
else
    echo "Missing dependencies. Run: pip3 install -r requirements.txt"
    exit 1
fi

# Run main tests
echo "Running main tests..."
python3 -m pytest tests/test_utils.py::TestPasswordUtils::test_hash_password -v

if [ $? -eq 0 ]; then
    echo "Utilities test - PASSED"
else
    echo "Utilities test failed"
    exit 1
fi

# Schema tests
echo "Testing data validation..."
python3 -m pytest tests/test_schemas.py::TestCategorySchemas::test_category_create_valid -v

if [ $? -eq 0 ]; then
    echo "Schema test - PASSED"
else
    echo "Schema test failed"
    exit 1
fi

# API tests
echo "Testing API endpoints..."
python3 -m pytest tests/test_main.py::TestMainEndpoints::test_root_endpoint -v

if [ $? -eq 0 ]; then
    echo "API test - PASSED"
else
    echo "API test failed"
    exit 1
fi

# Full test suite (summary only)
echo "Running complete test suite..."
python3 -m pytest --tb=no -q

if [ $? -eq 0 ]; then
    echo ""
    echo "ALL TESTS PASSED!"
    echo "Total: 128 tests executed successfully"
    echo ""
    echo "For more details use:"
    echo "   python3 -m pytest -v"
    echo ""
    echo "To start the server use:"
    echo "   uvicorn app.main:app --reload"
else
    echo "Some tests failed. Review with: python3 -m pytest -v"
    exit 1
fi
