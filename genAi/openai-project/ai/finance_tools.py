from .web_search import call_web_search

def get_stock_price(symbol):
    """Get current stock/crypto price using web search"""
    query = f"What is the current price of {symbol} stock or cryptocurrency today?"
    return call_web_search(query)

def get_exchange_rate(from_currency, to_currency):
    """Get current exchange rate between currencies"""
    query = f"What is the current exchange rate from {from_currency} to {to_currency}?"
    return call_web_search(query)

def get_company_news(company):
    """Get latest news about a company"""
    query = f"Latest financial news about {company} company today"
    return call_web_search(query)

finance_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get current stock or cryptocurrency price",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol or crypto name (e.g., AAPL, Bitcoin, Tesla)"}
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "get_exchange_rate",
            "description": "Get exchange rate between two currencies",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_currency": {"type": "string", "description": "Source currency (e.g., USD, EUR)"},
                    "to_currency": {"type": "string", "description": "Target currency (e.g., INR, JPY)"}
                },
                "required": ["from_currency", "to_currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_company_news", 
            "description": "Get latest financial news about a company",
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {"type": "string", "description": "Company name (e.g., Apple, Tesla, Microsoft)"}
                },
                "required": ["company"]
            }
        }
    }
]