"""Unit tests for the fake cost-data generators.

These don't touch the database: they only check that each generator returns
well-formed records for the requested dates.
"""
import datetime

import pytest

from aws.generate import AWSGenerator
from azure.generate import AzureExtractor
from gcp.generate import GCPGenerator
from lib.consts import USAGE_FAM_MAPPING
from rn.generate import RNGenerator

DATE = datetime.date(2025, 1, 15)


def expected_dates(days):
    return {(DATE - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)}


@pytest.mark.parametrize("days", [1, 3])
def test_aws_covers_each_requested_day(days):
    rows = AWSGenerator(DATE).generate_data(days=days)["results"]
    assert {r["invoice_date"] for r in rows} == expected_dates(days)


def test_aws_records_are_valid():
    rows = AWSGenerator(DATE).generate_data(days=1)["results"]

    assert len(rows) >= 1
    for r in rows:
        assert r["vendor"] == "AWS"
        assert 100 <= r["cost"] <= 500
        assert r["service_name"] in USAGE_FAM_MAPPING
        assert r["usage_family"] == USAGE_FAM_MAPPING[r["service_name"]]


def test_aws_daily_total_is_capped():
    """Generator stops adding rows once a day's total reaches 8000 (+ at most one row)."""
    rows = AWSGenerator(DATE).generate_data(days=1)["results"]
    assert sum(r["cost"] for r in rows) < 8000 + 500


def test_gcp_records_are_valid():
    rows = GCPGenerator(DATE).generate_data(days=2)["results"]

    assert {r["Invoice Date"] for r in rows} == expected_dates(2)
    for r in rows:
        assert 10 <= r["Cost"] <= 1000
        assert r["Project ID"].startswith("proj-")


def test_rn_records_are_valid():
    rows = RNGenerator(DATE).generate_data(days=1)["results"]

    assert len(rows) >= 1
    for r in rows:
        assert r["UsageEndDate"] == DATE.strftime("%Y-%m-%d")
        assert r["MonthYear"] == "2025-01-01"


def test_azure_dataframe_shape(monkeypatch):
    # The extractor sleeps 1s per subscription to mimic an API; skip that in tests.
    monkeypatch.setattr("azure.generate.time.sleep", lambda _: None)

    df = AzureExtractor(DATE).extract_data(days=2)

    assert not df.empty
    assert set(df["Invoice Date"]) == expected_dates(2)
    assert df["Cost"].between(10, 500).all()
    # Account names have any "(...)" suffix stripped
    assert not df["Account Name"].str.contains(r"\(").any()
