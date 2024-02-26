import os
from pathlib import Path
import polars as pl


class CachedDataset:
    """A base class for datasets that are cached locally."""

    def to_df(self) -> pl.DataFrame:
        """
        Converts the dataset to a Polars DataFrame.

        Returns:
            pl.DataFrame: The dataset as a Polars DataFrame.
        """

        cache = Path(os.environ.get("AIONDATA_CACHE", Path("~/.aiondata"))).expanduser()
        if hasattr(self, "COLLECTION"):
            cache = cache / self.COLLECTION
        cache.mkdir(parents=True, exist_ok=True)
        cache = cache / f"{self.__class__.__name__.lower()}.parquet"
        if cache.exists():
            return pl.read_parquet(cache)
        else:
            df = self.get_df()
            df.write_parquet(cache)
            return df


class CsvDataset(CachedDataset):
    """A base class for datasets that are stored in CSV format."""

    def get_df(self) -> pl.DataFrame:
        return pl.read_csv(self.SOURCE)


class ExcelDataset(CachedDataset):
    """A base class for datasets that are stored in Excel format."""

    def get_df(self) -> pl.DataFrame:
        return pl.read_excel(self.SOURCE)


class GeneratedDataset(CachedDataset):
    """A base class for datasets that are generated on-the-fly."""

    def get_df(self) -> pl.DataFrame:
        return pl.DataFrame(self.to_generator())
