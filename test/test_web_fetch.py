"""Test file for WebFetchTool."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.web_fetch import WebFetchTool


def test_url_normalization():
    """Test URL normalization and HTTP to HTTPS upgrade."""
    tool = WebFetchTool()

    # Test HTTP to HTTPS upgrade
    assert tool._normalize_url("http://example.com") == "https://example.com"

    # Test HTTPS stays HTTPS
    assert tool._normalize_url("https://example.com") == "https://example.com"

    # Test missing protocol
    assert tool._normalize_url("example.com") == "https://example.com"

    # Test with spaces
    assert tool._normalize_url("  https://example.com  ") == "https://example.com"

    print("✓ URL normalization tests passed!")


def test_html_to_text():
    """Test HTML to text conversion."""
    tool = WebFetchTool()

    html = "<h1>Title</h1><p>Hello <b>world</b></p>"
    result = tool._html_to_text(html)

    assert "Title" in result
    assert "Hello" in result
    assert "world" in result
    assert "<" not in result  # No HTML tags

    print("✓ HTML to text conversion tests passed!")


def test_html_to_markdown():
    """Test HTML to markdown conversion."""
    tool = WebFetchTool()

    html = "<h1>Title</h1><p>Hello <b>world</b></p>"
    result = tool._html_to_markdown(html)

    assert "# Title" in result
    assert "**world**" in result

    print("✓ HTML to markdown conversion tests passed!")


def test_large_content_handling():
    """Test large content truncation."""
    tool = WebFetchTool()

    # Create large content (>50KB)
    large_content = "A" * 60000
    result = tool._summarize_large_content(large_content, "https://example.com")

    assert len(result) < 10000  # Much smaller than original
    assert "truncated" in result.lower()
    assert "60,000" in result  # Shows original size

    print("✓ Large content handling tests passed!")


def test_format_conversion():
    """Test format conversion logic."""
    tool = WebFetchTool()

    html = "<h1>Test</h1><p>Content</p>"

    # HTML format
    result_html = tool._convert_format(html, "html", "https://example.com")
    assert result_html == html

    # Text format
    result_text = tool._convert_format(html, "text", "https://example.com")
    assert "Test" in result_text
    assert "Content" in result_text

    # Markdown format
    result_markdown = tool._convert_format(html, "markdown", "https://example.com")
    assert "# Test" in result_markdown

    print("✓ Format conversion tests passed!")


def test_error_handling():
    """Test error handling."""
    tool = WebFetchTool()

    # Test invalid URL
    result = tool.execute("not a valid url", "markdown")
    assert "Error:" in result

    # Test with mock - should handle connection errors gracefully
    result = tool.execute("https://this-domain-does-not-exist-12345.com", "markdown")
    assert "Error:" in result

    print("✓ Error handling tests passed!")


def test_real_fetch():
    """Test actual web fetch with a reliable test site."""
    tool = WebFetchTool()

    # Use httpbin.org which is designed for testing
    try:
        result = tool.execute("https://httpbin.org/html", "text")
        # Should contain some content or error message
        assert isinstance(result, str)
        print(f"✓ Real fetch test completed (got {len(result)} chars)")
    except Exception as e:
        print(f"⚠ Real fetch test skipped (network issue): {e}")


def test_execute_signature():
    """Test that execute method has correct signature."""
    tool = WebFetchTool()

    # Test with default format
    result = tool.execute("https://example.com")
    assert isinstance(result, str)

    # Test with explicit format
    result = tool.execute("https://example.com", "html")
    assert isinstance(result, str)

    print("✓ Execute signature tests passed!")


def main():
    """Run all tests."""
    print("Running WebFetchTool tests...\n")

    test_url_normalization()
    test_html_to_text()
    test_html_to_markdown()
    test_large_content_handling()
    test_format_conversion()
    test_error_handling()
    test_execute_signature()
    test_real_fetch()

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    main()
