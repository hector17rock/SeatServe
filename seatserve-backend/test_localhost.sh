#!/bin/bash

BASE_URL="http://localhost:8000"

echo "Testing SeatServe API on localhost:8000"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Server URLs:${NC}"
echo "   API Root: http://localhost:8000/"
echo "   Interactive Docs: http://localhost:8000/docs"
echo "   OpenAPI Schema: http://localhost:8000/redoc"
echo ""

# Test 1: Root endpoint
echo -e "${YELLOW}1. Testing Root Endpoint${NC}"
echo "GET $BASE_URL/"
curl -s $BASE_URL/ | python3 -m json.tool
echo ""

# Test 2: Health check
echo -e "${YELLOW}2. Testing Health Check${NC}"
echo "GET $BASE_URL/health"
curl -s $BASE_URL/health | python3 -m json.tool
echo ""

# Test 3: API Info
echo -e "${YELLOW}3. Testing API Info${NC}"
echo "GET $BASE_URL/api/v1/info"
curl -s $BASE_URL/api/v1/info | python3 -m json.tool
echo ""

# Test 4: Get Categories (should be empty initially)
echo -e "${YELLOW}4. Testing Get Categories${NC}"
echo "GET $BASE_URL/api/v1/menu/categories"
curl -s $BASE_URL/api/v1/menu/categories | python3 -m json.tool
echo ""

# Test 5: Create a Category
echo -e "${YELLOW}5. Testing Create Category${NC}"
echo "POST $BASE_URL/api/v1/menu/categories"
CATEGORY_RESPONSE=$(curl -s -X POST $BASE_URL/api/v1/menu/categories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Beverages",
    "description": "Hot and cold drinks",
    "is_active": true,
    "sort_order": 1
  }')
echo "$CATEGORY_RESPONSE" | python3 -m json.tool
CATEGORY_ID=$(echo "$CATEGORY_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null || echo "1")
echo ""

# Test 6: Create another Category
echo -e "${YELLOW}6. Testing Create Another Category${NC}"
echo "POST $BASE_URL/api/v1/menu/categories"
curl -s -X POST $BASE_URL/api/v1/menu/categories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Main Courses",
    "description": "Delicious main dishes",
    "is_active": true,
    "sort_order": 2
  }' | python3 -m json.tool
echo ""

# Test 7: Get Categories (should now have items)
echo -e "${YELLOW}7. Testing Get Categories (Updated)${NC}"
echo "GET $BASE_URL/api/v1/menu/categories"
curl -s $BASE_URL/api/v1/menu/categories | python3 -m json.tool
echo ""

# Test 8: Create a Menu Item
echo -e "${YELLOW}8. Testing Create Menu Item${NC}"
echo "POST $BASE_URL/api/v1/menu/items"
MENU_ITEM_RESPONSE=$(curl -s -X POST $BASE_URL/api/v1/menu/items \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Cappuccino\",
    \"description\": \"Rich espresso with steamed milk foam\",
    \"price\": 4.50,
    \"category_id\": $CATEGORY_ID,
    \"is_available\": true,
    \"is_vegetarian\": true,
    \"calories\": 120,
    \"preparation_time\": 5
  }")
echo "$MENU_ITEM_RESPONSE" | python3 -m json.tool
MENU_ITEM_ID=$(echo "$MENU_ITEM_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null || echo "1")
echo ""

# Test 9: Get Menu Items
echo -e "${YELLOW}9. Testing Get Menu Items${NC}"
echo "GET $BASE_URL/api/v1/menu/items"
curl -s $BASE_URL/api/v1/menu/items | python3 -m json.tool
echo ""

# Test 10: Get Specific Category
echo -e "${YELLOW}10. Testing Get Specific Category${NC}"
echo "GET $BASE_URL/api/v1/menu/categories/$CATEGORY_ID"
curl -s $BASE_URL/api/v1/menu/categories/$CATEGORY_ID | python3 -m json.tool
echo ""

# Test 11: Get Specific Menu Item
echo -e "${YELLOW}11. Testing Get Specific Menu Item${NC}"
echo "GET $BASE_URL/api/v1/menu/items/$MENU_ITEM_ID"
curl -s $BASE_URL/api/v1/menu/items/$MENU_ITEM_ID | python3 -m json.tool
echo ""

# Test 12: Update Category
echo -e "${YELLOW}12. Testing Update Category${NC}"
echo "PUT $BASE_URL/api/v1/menu/categories/$CATEGORY_ID"
curl -s -X PUT $BASE_URL/api/v1/menu/categories/$CATEGORY_ID \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hot & Cold Beverages",
    "description": "Premium hot and cold drinks selection"
  }' | python3 -m json.tool
echo ""

# Test 13: Search Menu Items
echo -e "${YELLOW}13. Testing Search Menu Items${NC}"
echo "GET $BASE_URL/api/v1/menu/items?search=cappuccino"
curl -s "$BASE_URL/api/v1/menu/items?search=cappuccino" | python3 -m json.tool
echo ""

# Test 14: Filter by Category
echo -e "${YELLOW}14. Testing Filter Items by Category${NC}"
echo "GET $BASE_URL/api/v1/menu/items?category_id=$CATEGORY_ID"
curl -s "$BASE_URL/api/v1/menu/items?category_id=$CATEGORY_ID" | python3 -m json.tool
echo ""

# Test 15: Pagination Test
echo -e "${YELLOW}15. Testing Pagination${NC}"
echo "GET $BASE_URL/api/v1/menu/categories?skip=0&limit=1"
curl -s "$BASE_URL/api/v1/menu/categories?skip=0&limit=1" | python3 -m json.tool
echo ""

echo -e "${GREEN}All tests completed!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "   • Open browser to http://localhost:8000/docs for interactive API docs"
echo "   • Use http://localhost:8000/redoc for alternative documentation"
echo "   • API is running and ready for your frontend application"
echo ""
echo -e "${BLUE}To stop the server:${NC}"
echo "   • Press Ctrl+C if running in foreground"
echo "   • Or run: pkill -f uvicorn"