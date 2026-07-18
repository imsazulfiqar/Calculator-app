import unittest

from fastapi.testclient import TestClient

from learn import app


class CalculatorAppTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_homepage_serves_ui(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Calculator", response.text)

    def test_calc_endpoint_returns_json(self):
        response = self.client.post(
            "/api/calc",
            json={"expression": "2 + 3 * 4"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"], 14.0)


if __name__ == "__main__":
    unittest.main()
