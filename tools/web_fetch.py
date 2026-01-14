"""Web fetch tool for retrieving content from URLs."""
import urllib.request
import urllib.error
from typing import Dict, Any
import re

from .base import BaseTool


class WebFetchTool(BaseTool):
    """Fetch content from URLs and convert to various formats."""

    @property
    def name(self) -> str:
        return "web_fetch"

    @property
    def description(self) -> str:
        return "Fetch content from a URL and convert to specified format (markdown, text, or HTML)"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "url": {
                "type": "string",
                "description": "URL to fetch content from (HTTP will be auto-upgraded to HTTPS)"
            },
            "format": {
                "type": "string",
                "enum": ["markdown", "text", "html"],
                "description": "Output format - markdown by default",
                "default": "markdown"
            }
        }

    def execute(self, url: str, format: str = "markdown") -> str:
        """Execute web fetch with format conversion."""
        try:
            # Validate and normalize URL
            url = self._normalize_url(url)

            # Fetch content
            content = self._fetch_url(url)

            # Convert to requested format
            return self._convert_format(content, format, url)

        except Exception as e:
            return f"Error: {str(e)}"

    def _normalize_url(self, url: str) -> str:
        """Normalize URL - auto-upgrade HTTP to HTTPS."""
        url = url.strip()

        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # Upgrade HTTP to HTTPS
        if url.startswith('http://'):
            url = 'https://' + url[7:]

        return url

    def _fetch_url(self, url: str) -> str:
        """Fetch content from URL with proper headers."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AgenticLoop/1.0)'
        }

        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()

            # Try to decode as UTF-8, fallback to latin-1
            try:
                return content.decode('utf-8')
            except UnicodeDecodeError:
                return content.decode('latin-1')

    def _convert_format(self, content: str, format: str, url: str) -> str:
        """Convert content to requested format."""
        # Handle large content
        if len(content) > 50000:  # 50KB threshold
            content = self._summarize_large_content(content, url)

        if format == "html":
            return content

        if format == "text":
            return self._html_to_text(content)

        if format == "markdown":
            return self._html_to_markdown(content)

        return content

    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text."""
        # Remove script and style content
        html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        return text

    def _html_to_markdown(self, html: str) -> str:
        """Convert HTML to markdown format."""
        # Try to use html2text if available
        try:
            from html2text import html2text
            return html2text(html)
        except ImportError:
            # Fallback: basic conversion
            return self._basic_html_to_markdown(html)

    def _basic_html_to_markdown(self, html: str) -> str:
        """Basic HTML to markdown conversion without external libraries."""
        # Remove script and style
        html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

        # Headers
        html = re.sub(r'<h1.*?>(.*?)</h1>', r'# \1\n\n', html, flags=re.IGNORECASE)
        html = re.sub(r'<h2.*?>(.*?)</h2>', r'## \1\n\n', html, flags=re.IGNORECASE)
        html = re.sub(r'<h3.*?>(.*?)</h3>', r'### \1\n\n', html, flags=re.IGNORECASE)

        # Bold and italic
        html = re.sub(r'<strong>(.*?)</strong>', r'**\1**', html, flags=re.IGNORECASE)
        html = re.sub(r'<b>(.*?)</b>', r'**\1**', html, flags=re.IGNORECASE)
        html = re.sub(r'<em>(.*?)</em>', r'*\1*', html, flags=re.IGNORECASE)
        html = re.sub(r'<i>(.*?)</i>', r'*\1*', html, flags=re.IGNORECASE)

        # Links
        html = re.sub(r'<a href="(.*?)".*?>(.*?)</a>', r'[\2](\1)', html, flags=re.IGNORECASE)

        # Lists
        html = re.sub(r'<li>(.*?)</li>', r'- \1\n', html, flags=re.IGNORECASE)

        # Paragraphs
        html = re.sub(r'<p>(.*?)</p>', r'\1\n\n', html, flags=re.IGNORECASE)

        # Line breaks
        html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)

        # Remove remaining tags
        html = re.sub(r'<[^>]+>', '', html)

        # Clean up whitespace
        html = re.sub(r'\n{3,}', '\n\n', html)
        html = html.strip()

        return html

    def _summarize_large_content(self, content: str, url: str) -> str:
        """Summarize large content."""
        truncated = content[:5000]  # Keep first 5KB

        note = f"\n\n---\n**Note**: Content truncated from {len(content):,} bytes to 5,000 bytes for brevity.\n"
        note += f"URL: {url}\n"
        note += "Consider requesting a more specific page or section if needed."

        return truncated + note
