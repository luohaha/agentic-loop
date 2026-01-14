"""Example usage of WebFetchTool."""
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.web_fetch import WebFetchTool
from tools.web_search import WebSearchTool


def main():
    """Run WebFetchTool examples."""
    print("=" * 70)
    print("WebFetchTool Usage Examples")
    print("=" * 70)

    # Initialize tools
    fetch_tool = WebFetchTool()
    search_tool = WebSearchTool()

    # Example 1: Basic fetch with default format (markdown)
    print("\n--- Example 1: Basic Fetch (Markdown) ---")
    print("URL: https://httpbin.org/html")
    result = fetch_tool.execute("https://httpbin.org/html")
    print(f"Result (first 300 chars):\n{result[:300]}...")

    # Example 2: Different formats
    print("\n\n--- Example 2: Format Options ---")
    url = "https://httpbin.org/html"

    print("\n2a. HTML format:")
    html_result = fetch_tool.execute(url, "html")
    print(f"Result (first 200 chars):\n{html_result[:200]}...")

    print("\n2b. Text format:")
    text_result = fetch_tool.execute(url, "text")
    print(f"Result (first 200 chars):\n{text_result[:200]}...")

    print("\n2c. Markdown format:")
    md_result = fetch_tool.execute(url, "markdown")
    print(f"Result (first 200 chars):\n{md_result[:200]}...")

    # Example 3: URL normalization
    print("\n\n--- Example 3: URL Auto-Normalization ---")
    test_urls = [
        "http://httpbin.org/html",      # HTTP -> HTTPS
        "https://httpbin.org/html",     # Already HTTPS
        "httpbin.org/html",             # No protocol
    ]

    for test_url in test_urls:
        result = fetch_tool.execute(test_url, "text")
        status = "✓ Success" if "Error" not in result else "✗ Failed"
        print(f"  {test_url:30} -> {status}")

    # Example 4: Error handling
    print("\n\n--- Example 4: Error Handling ---")

    print("\n4a. Invalid URL format:")
    result = fetch_tool.execute("not-a-valid-url", "text")
    print(f"  Result: {result}")

    print("\n4b. Non-existent domain:")
    result = fetch_tool.execute("https://does-not-exist-12345.com", "text")
    print(f"  Result: {result[:80]}...")

    # Example 5: Comparison with WebSearchTool
    print("\n\n--- Example 5: WebFetchTool vs WebSearchTool ---")

    print("\nWebSearchTool (search engine):")
    search_result = search_tool.execute("python web scraping")
    print(f"  Input: 'python web scraping' (search query)")
    print(f"  Output: {len(search_result)} chars of search results")
    print(f"  Preview: {search_result[:100]}...")

    print("\nWebFetchTool (direct fetch):")
    fetch_result = fetch_tool.execute("https://httpbin.org/html", "text")
    print(f"  Input: 'https://httpbin.org/html' (specific URL)")
    print(f"  Output: {len(fetch_result)} chars of page content")
    print(f"  Preview: {fetch_result[:100]}...")

    # Example 6: Tool schema
    print("\n\n--- Example 6: Tool Schema ---")
    schema = fetch_tool.to_anthropic_schema()
    print(f"  Name: {schema['name']}")
    print(f"  Description: {schema['description']}")
    print(f"  Required params: {schema['input_schema']['required']}")
    print(f"  Format enum: {schema['input_schema']['properties']['format']['enum']}")
    print(f"  Format default: {schema['input_schema']['properties']['format']['default']}")

    # Example 7: Real-world use case
    print("\n\n--- Example 7: Real-World Use Case ---")
    print("Scenario: You need to quickly check the content of a documentation page")
    print("Task: Fetch and summarize https://httpbin.org/html")

    result = fetch_tool.execute("https://httpbin.org/html", "markdown")
    print(f"\nFetched content (markdown):\n{result[:400]}...")
    print(f"\nTotal length: {len(result)} characters")

    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
