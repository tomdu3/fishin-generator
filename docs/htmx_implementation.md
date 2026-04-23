# Implementation Plan - Introduce HTMX for Dynamic Frontend

The goal is to make the Phishing Simulator frontend dynamic using HTMX. This will allow the dashboard and campaign details to update automatically when database changes occur (e.g., when an email is opened or clicked) and improve the user experience for managing targets.

## User Review Required

> [!IMPORTANT]
> The plan uses polling (every 5 seconds) for real-time updates. This is a simple and effective way to show database changes without complex WebSocket setups.

## Proposed Changes

### Core Integration

#### [MODIFY] [base.html](file:///home/tom/projects/fishin-generator/templates/base.html)
- Add HTMX script tag to the `<head>`.

### Dashboard Polling

#### [NEW] [dashboard_stats.html](file:///home/tom/projects/fishin-generator/templates/partials/dashboard_stats.html)
- Extract the total counts into a partial.

#### [NEW] [campaign_list.html](file:///home/tom/projects/fishin-generator/templates/partials/campaign_list.html)
- Extract the campaign table into a partial.

#### [MODIFY] [dashboard.html](file:///home/tom/projects/fishin-generator/templates/dashboard.html)
- Replace static content with HTMX polling targets.

#### [MODIFY] [app.py](file:///home/tom/projects/fishin-generator/app.py)
- Add routes to return the partials.

### Campaign Details Polling

#### [NEW] [campaign_stats.html](file:///home/tom/projects/fishin-generator/templates/partials/campaign_stats.html)
- Extract the stats cards into a partial.

#### [NEW] [event_list.html](file:///home/tom/projects/fishin-generator/templates/partials/event_list.html)
- Extract the tracking events table into a partial.

#### [MODIFY] [campaign_details.html](file:///home/tom/projects/fishin-generator/templates/campaign_details.html)
- Replace static content with HTMX polling targets.

### Target Management

#### [MODIFY] [targets.html](file:///home/tom/projects/fishin-generator/templates/targets.html)
- Update the form to use `hx-post` and target the target list.
- Update delete buttons to use `hx-post` with confirmation.

#### [NEW] [target_list.html](file:///home/tom/projects/fishin-generator/templates/partials/target_list.html)
- Extract the target list into a partial for reuse.

## Verification Plan

### Manual Verification
1. Open the dashboard and verify that it polls for updates.
2. Open a campaign details page, simulate an email open/click (via the tracking URLs), and verify that the stats update automatically.
3. Add and delete targets on the `/targets` page and verify they update without a full page reload.
