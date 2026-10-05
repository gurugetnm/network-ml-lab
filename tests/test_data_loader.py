"""Small tests using temporary synthetic CSVs; no dataset download required."""
import tempfile
import unittest
from pathlib import Path

from src.data_loader import load_dataset


class DatasetLoaderTests(unittest.TestCase):
    def test_load_preserves_rows_and_missing_values(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "UNSW_NB15_training-set.csv"
            path.write_text("id,dur,label\n1,,0\n2,0.5,1\n2,0.5,1\n")
            data = load_dataset(data_dir=directory)
            self.assertEqual(data.shape, (3, 3))
            self.assertTrue(data["dur"].isna().iloc[0])
            self.assertEqual(data.duplicated().sum(), 1)

    def test_missing_file_has_setup_hint(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FileNotFoundError, "data/raw"):
                load_dataset(data_dir=directory)

    def test_invalid_split(self):
        with self.assertRaisesRegex(ValueError, "split"):
            load_dataset(split="validation")

    def test_invalid_schema_and_target(self):
        for csv_text in ["dur\n1\n", "label\n2\n", "label,dur\n,1\n", "label\n"]:
            with self.subTest(csv_text=csv_text), tempfile.TemporaryDirectory() as directory:
                (Path(directory) / "UNSW_NB15_training-set.csv").write_text(csv_text)
                with self.assertRaises(ValueError):
                    load_dataset(data_dir=directory)


if __name__ == "__main__":
    unittest.main()
