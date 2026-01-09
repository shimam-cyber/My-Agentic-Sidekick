import os
import requests
import subprocess
import sys
from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from dotenv import load_dotenv
from langchain.agents import Tool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_experimental.tools import PythonREPLTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper



load_dotenv(override=True)
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"
serper = GoogleSerperAPIWrapper()

async def playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright


def push(text: str):
    """Send a push notification to the user"""
    requests.post(pushover_url, data = {"token": pushover_token, "user": pushover_user, "message": text})
    return "success"


def get_file_tools():
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()


async def other_tools():
    push_tool = Tool(name="send_push_notification", func=push, description="Use this tool when you want to send a push notification")
    file_tools = get_file_tools()

    tool_search =Tool(
        name="search",
        func=serper.run,
        description="Use this tool when you want to get the results of an online web search"
    )

    wikipedia = WikipediaAPIWrapper()
    wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)

    python_repl = PythonREPLTool()
    
    return file_tools + [push_tool, tool_search, python_repl,  wiki_tool]


def ensure_playwright_installed():
    """Ensure Playwright browsers are installed at runtime if not present."""
    chromium_path = "/root/.cache/ms-playwright/chromium-1169"
    chromium_headless_path = "/root/.cache/ms-playwright/chromium_headless_shell-1169"
    
    if not os.path.exists(chromium_path) and not os.path.exists(chromium_headless_path):
        print("Playwright browsers not found. Installing...", file=sys.stderr)
        try:
            result = subprocess.run(
                ["playwright", "install", "--with-deps", "chromium"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            if result.returncode == 0:
                print("Playwright browsers installed successfully!", file=sys.stderr)
            else:
                print(f"Playwright installation failed: {result.stderr}", file=sys.stderr)
                raise Exception(f"Playwright installation failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("Playwright installation timed out", file=sys.stderr)
            raise
        except Exception as e:
            print(f"Failed to install Playwright browsers: {e}", file=sys.stderr)
            raise


async def playwright_tools():
    """Initialize Playwright and return browser tools."""
    try:
        # Try to ensure browsers are installed
        ensure_playwright_installed()
        
        # Import and start Playwright
        from playwright.async_api import async_playwright
        
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        
        # Create your tools here based on your actual implementation
        # This is a placeholder - replace with your actual tool creation
        tools = []  
        
        print("Playwright initialized successfully", file=sys.stderr)
        return tools, browser, playwright
        
    except Exception as e:
        print(f"WARNING: Playwright initialization failed: {e}", file=sys.stderr)
        print("The app will continue without browser automation capabilities", file=sys.stderr)
        
        # Return empty/None values so the app can still start
        return [], None, None


# Add any other tool functions you have below
# Make sure they handle the case where browser is None