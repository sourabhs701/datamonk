import json
from ai.api_call import call_api
from ai.finance_tools import get_stock_price, get_exchange_rate, get_company_news, finance_tools



def main():
    print("Finance Assistant Bot")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye! 👋")
            break
            
        if not user_input:
            continue
            
        try:
            
            messages = [{"role": "user", "content": user_input}]
            result = call_api(messages, finance_tools)
            
            
            tool_calls = result.choices[0].message.tool_calls
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    if function_name == "get_stock_price":
                        tool_result = get_stock_price(args["symbol"])
                    elif function_name == "get_exchange_rate":
                        tool_result = get_exchange_rate(args["from_currency"], args["to_currency"])
                    elif function_name == "get_company_news":
                        tool_result = get_company_news(args["company"])
                    
                    
                    messages.append({
                        "role": "user",
                        "content": tool_result
                    })

                
                print("Bot:", tool_result)
            else:
                print("Bot:", result.choices[0].message.content)
                
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    main()
