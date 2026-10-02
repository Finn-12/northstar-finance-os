import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = str(Path(__file__).resolve().parents[1] / "src" / "dashboards" / "streamlit_app.py")


class MonthlyUpdateAppTests(unittest.TestCase):
    def test_subconsultant_actual_compares_with_synthetic_prior_month(self) -> None:
        app = AppTest.from_file(APP_PATH, default_timeout=10).run()

        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox[1].value, "Supplier A")
        self.assertTrue(
            any("Prior-period value (2026-09): CU 1,000.00" in item.value for item in app.caption)
        )

        app.number_input[0].set_value(1250.0)
        app.button[0].click().run()

        self.assertFalse(app.exception)
        self.assertTrue(
            any("cost increased by **CU 250.00**" in item.value for item in app.markdown)
        )
        self.assertTrue(
            any("margin impact depends on Finance-approved" in item.value for item in app.info)
        )
        self.assertTrue(any("Draft saved" in item.value for item in app.success))

    def test_new_supplier_does_not_get_a_fabricated_variance(self) -> None:
        app = AppTest.from_file(APP_PATH, default_timeout=10).run()
        app.selectbox[1].select("New supplier (no prior history)").run()
        app.number_input[0].set_value(500.0)
        app.button[0].click().run()

        self.assertFalse(app.exception)
        self.assertTrue(
            any("No comparable prior-period value is available" in item.value for item in app.info)
        )

    def test_unimplemented_topic_is_clearly_deferred(self) -> None:
        app = AppTest.from_file(APP_PATH, default_timeout=10).run()
        app.selectbox[0].select("Client / scope").run()

        self.assertFalse(app.exception)
        self.assertTrue(
            any("Client / scope updates are planned for a later MVP iteration." in item.value
                for item in app.info)
        )


if __name__ == "__main__":
    unittest.main()
