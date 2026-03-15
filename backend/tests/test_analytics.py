import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_dashboard_stats(client: AsyncClient, admin_headers, sample_deal):
    response = await client.get("/api/v1/dashboard/stats", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_contacts" in data
    assert "total_deals" in data
    assert "total_revenue" in data
    assert "pipeline_value" in data


@pytest.mark.asyncio
async def test_pipeline_summary(client: AsyncClient, admin_headers, sample_deal):
    response = await client.get("/api/v1/dashboard/pipeline-summary", headers=admin_headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_revenue_forecast(client: AsyncClient, admin_headers):
    response = await client.get("/api/v1/reports/revenue-forecast?months=3", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_pipeline_velocity(client: AsyncClient, admin_headers, sample_stages):
    response = await client.get("/api/v1/reports/pipeline-velocity", headers=admin_headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_deal_value_by_month(client: AsyncClient, admin_headers):
    response = await client.get("/api/v1/dashboard/deal-value-by-month?months=6", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) == 6


@pytest.mark.asyncio
async def test_contacts_by_source(client: AsyncClient, admin_headers, sample_contact):
    response = await client.get("/api/v1/dashboard/contacts-by-source", headers=admin_headers)
    assert response.status_code == 200
