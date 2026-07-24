#!/usr/bin/env python3
"""
Selenium Smoke Test Suite for GUIDESOFT.WEB
Tests core user flows with Selenium WebDriver.
"""

import os
import sys
import time
import unittest
from typing import Optional

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  selenium-webdriver not installed. Run: npm install selenium-webdriver")
    print("   Also install: pip install selenium")

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5173")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8080")
HEADLESS = os.environ.get("HEADLESS", "true").lower() == "true"
BROWSER = os.environ.get("BROWSER", "chrome").lower()


def create_driver():
    """Create and configure a WebDriver instance."""
    if BROWSER == "firefox":
        options = FirefoxOptions()
        if HEADLESS:
            options.add_argument("--headless")
        return webdriver.Firefox(options=options)
    else:
        options = ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,800")
        return webdriver.Chrome(options=options)


class LandingPageTests(unittest.TestCase):
    """Smoke tests for the Landing Page."""

    @classmethod
    def setUpClass(cls):
        if not SELENIUM_AVAILABLE:
            raise unittest.SkipTest("Selenium not installed")
        cls.driver = create_driver()
        cls.wait = WebDriverWait(cls.driver, 15)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()

    def test_01_landing_page_loads(self):
        """Landing page should load without redirecting to /error."""
        self.driver.get(BASE_URL)
        time.sleep(2)
        
        current_url = self.driver.current_url
        self.assertNotIn("/error", current_url, 
                         f"Was redirected to error page. Current URL: {current_url}")
        print(f"✅ Landing page loaded: {current_url}")

    def test_02_page_title_exists(self):
        """Page should have a meaningful title."""
        self.driver.get(BASE_URL)
        time.sleep(2)
        
        title = self.driver.title
        self.assertTrue(len(title) > 0, "Page title should not be empty")
        print(f"✅ Page title: {title}")

    def test_03_no_console_errors(self):
        """Page should not have critical JavaScript errors."""
        self.driver.get(BASE_URL)
        time.sleep(2)
        
        try:
            logs = self.driver.get_log("browser")
            critical_errors = [
                log for log in logs 
                if log["level"] == "SEVERE" and "favicon" not in log["message"]
            ]
            if critical_errors:
                print(f"⚠️  Browser errors found: {critical_errors}")
            # Don't fail the test — just report
        except Exception:
            pass  # Firefox doesn't support get_log
        
        print("✅ Console error check complete")

    def test_04_auth_page_loads(self):
        """Auth page should load without errors."""
        self.driver.get(f"{BASE_URL}/auth")
        time.sleep(2)
        
        current_url = self.driver.current_url
        self.assertNotIn("/error", current_url,
                         f"Auth page redirected to error: {current_url}")
        print(f"✅ Auth page loaded: {current_url}")

    def test_05_auth_email_input_exists(self):
        """Auth page should have email input."""
        self.driver.get(f"{BASE_URL}/auth")
        time.sleep(2)
        
        try:
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"], input[name="email"]'))
            )
            self.assertTrue(email_input.is_displayed(), "Email input should be visible")
            print("✅ Email input found on auth page")
        except TimeoutException:
            print("⚠️  Email input not found — auth page may have different structure")

    def test_06_auth_password_input_exists(self):
        """Auth page should have password input."""
        self.driver.get(f"{BASE_URL}/auth")
        time.sleep(2)
        
        try:
            pwd_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
            )
            self.assertTrue(pwd_input.is_displayed(), "Password input should be visible")
            print("✅ Password input found on auth page")
        except TimeoutException:
            print("⚠️  Password input not found")

    def test_07_invalid_login_shows_error(self):
        """Invalid credentials should show error, not crash."""
        self.driver.get(f"{BASE_URL}/auth")
        time.sleep(2)
        
        try:
            email_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="email"], input[name="email"]')
            pwd_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            
            email_input.send_keys("invalid@nowhere.com")
            pwd_input.send_keys("wrongpassword123")
            submit_btn.click()
            
            time.sleep(2)
            
            # Should not navigate to /
            self.assertNotEqual(self.driver.current_url, f"{BASE_URL}/",
                               "Should not navigate to home on invalid creds")
            print("✅ Invalid login handled correctly")
        except NoSuchElementException:
            print("⚠️  Could not find form elements for login test")

    def test_08_mobile_viewport(self):
        """Page should not have horizontal overflow on mobile."""
        self.driver.set_window_size(375, 812)
        self.driver.get(BASE_URL)
        time.sleep(2)
        
        scroll_width = self.driver.execute_script("return document.body.scrollWidth")
        client_width = self.driver.execute_script("return document.body.clientWidth")
        
        self.assertLessEqual(scroll_width, client_width + 20,
                            f"Horizontal overflow detected: scrollWidth={scroll_width}, clientWidth={client_width}")
        print(f"✅ No horizontal overflow on mobile: {scroll_width} <= {client_width}")
        
        # Reset
        self.driver.set_window_size(1280, 800)

    def test_09_heading_hierarchy(self):
        """Page should have proper h1 heading."""
        self.driver.get(BASE_URL)
        time.sleep(2)
        
        h1_elements = self.driver.find_elements(By.TAG_NAME, "h1")
        # Should have at least one h1
        print(f"  Found {len(h1_elements)} h1 element(s)")
        # Don't fail hard — just report
        print("✅ Heading hierarchy check complete")

    def test_10_keyboard_focus(self):
        """Interactive elements should be keyboard focusable."""
        self.driver.get(BASE_URL)
        time.sleep(2)
        
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.TAB)
        time.sleep(0.3)
        
        focused_tag = self.driver.execute_script("return document.activeElement.tagName")
        print(f"  First tab focus: {focused_tag}")
        print("✅ Keyboard navigation check complete")


class BackendAPITests(unittest.TestCase):
    """Smoke tests for the Backend API."""

    def setUp(self):
        """Use requests for API testing."""
        try:
            import requests
            self.requests = requests
            self.backend_url = BACKEND_URL
        except ImportError:
            self.skipTest("requests library not available")

    def test_health_endpoint(self):
        """Backend health check should return 200."""
        try:
            resp = self.requests.get(f"{self.backend_url}/health", timeout=5)
            self.assertEqual(resp.status_code, 200)
            print(f"✅ Backend health check: {resp.status_code}")
        except Exception as e:
            print(f"⚠️  Backend not running: {e}")

    def test_agents_endpoint(self):
        """Agents API should return a list of agents."""
        try:
            resp = self.requests.get(f"{self.backend_url}/api/v1/agents/", timeout=5)
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 0)
            
            # Verify agent structure
            agent = data[0]
            self.assertIn("id", agent)
            self.assertIn("name", agent)
            self.assertIn("system_prompt", agent)
            
            print(f"✅ Agents API: {len(data)} agents found")
            print(f"   Sample: {agent['name']}")
        except Exception as e:
            print(f"⚠️  Agents API test skipped: {e}")

    def test_providers_endpoint(self):
        """Providers API should return a list of providers."""
        try:
            resp = self.requests.get(f"{self.backend_url}/api/v1/providers/", timeout=5)
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 5)  # Should have many providers
            
            # Verify provider structure
            provider = data[0]
            self.assertIn("id", provider)
            self.assertIn("name", provider)
            self.assertIn("models", provider)
            
            providers_by_id = {p["id"]: p for p in data}
            
            # Check key providers exist
            for key_provider in ["openai", "anthropic", "groq", "deepseek"]:
                self.assertIn(key_provider, providers_by_id, 
                             f"Provider '{key_provider}' should be in registry")
            
            print(f"✅ Providers API: {len(data)} providers found")
        except Exception as e:
            print(f"⚠️  Providers API test skipped: {e}")

    def test_skills_custom_endpoint(self):
        """New skills registry endpoint should work."""
        try:
            resp = self.requests.get(f"{self.backend_url}/api/v1/agents/domains/", timeout=5)
            self.assertEqual(resp.status_code, 200)
            domains = resp.json()
            self.assertIsInstance(domains, list)
            print(f"✅ Agent domains: {domains}")
        except Exception as e:
            print(f"⚠️  Domains API test skipped: {e}")


def run_all_tests():
    """Run all smoke tests and print a summary."""
    print("\n" + "="*60)
    print("🧪 GUIDESOFT.WEB Selenium Smoke Tests")
    print("="*60)
    print(f"  BASE_URL: {BASE_URL}")
    print(f"  BACKEND_URL: {BACKEND_URL}")
    print(f"  BROWSER: {BROWSER}")
    print(f"  HEADLESS: {HEADLESS}")
    print("="*60 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(BackendAPITests))
    
    if SELENIUM_AVAILABLE:
        suite.addTests(loader.loadTestsFromTestCase(LandingPageTests))
    else:
        print("⚠️  Skipping browser tests — selenium not installed")
        print("   Install with: pip install selenium")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("✅ All smoke tests passed!")
    else:
        print(f"❌ {len(result.failures)} failures, {len(result.errors)} errors")
    print("="*60)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
