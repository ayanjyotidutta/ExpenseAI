# Spec: Profile Page Design

## Overview
This step transforms the existing functional-but-bare profile page into a polished, fully-designed dashboard. The `/profile` route and its template already exist with working data (expense list + total), but have minimal visual treatment. This step adds a summary stats bar, per-category spending breakdown with progress bars, an "Add Expense" call-to-action button, and responsive polish — giving users a clear, actionable view of their spending at a glance.

## Depends on
- Step 01 — Database Setup (users + expenses tables)
- Step 02 — Registration
- Step 03 — Login and Logout (session management, redirect guards)

## Routes
No new routes. The existing `GET /profile` route in `app.py` already fetches expenses and passes them to `profile.html`; it only needs a small update to also pass per-category totals.

## Database changes
No new tables or columns. A new `get_expenses_by_user` helper variant is not needed — category aggregation is done in the route from the existing query result.

## Templates
- **Modify:** `templates/profile.html` — full redesign of the page layout:
  - Add a stats bar (total spent, number of expenses, largest single expense)
  - Add a category breakdown section with labelled progress bars
  - Add an "Add Expense" CTA button (links to `url_for('add_expense')` stub)
  - Keep the existing expense table but style it more clearly with an "Actions" column placeholder (disabled, not wired up yet)
  - Flash messages remain in place

## Files to change
- `app.py` — update `profile()` route to compute and pass `stats` dict (total, count, max_expense, category_totals) to the template
- `templates/profile.html` — full redesign as described above
- `static/css/style.css` — add new CSS classes for the stats bar, category breakdown, and CTA button; use only CSS variables

## Files to create
None. All work fits within existing files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw SQLite via `get_db()` only
- Parameterised queries only — no f-strings in SQL
- Use CSS variables exclusively — never hardcode hex values
- All templates extend `base.html`
- Route function stays single-responsibility: compute stats dict, render template
- Category aggregation must be done in Python from the existing `expenses` list — no extra DB query
- The "Add Expense" button must use `url_for('add_expense')` — not a hardcoded URL
- Do not implement or wire up edit/delete actions — those are Steps 8 and 9

## Definition of done
- [ ] Visiting `/profile` while logged in shows a stats bar with: total spent, number of expenses, and the largest single expense amount
- [ ] A category breakdown section shows each category present in the user's expenses as a labelled progress bar, scaled relative to the largest category total
- [ ] An "Add Expense" button is visible and renders without error (clicking it returns the Step 7 stub string, which is acceptable)
- [ ] The existing expense table is still present with all rows and correct data
- [ ] Flash messages still appear when present
- [ ] The page renders correctly in both dark and light themes (toggle works)
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] No hardcoded hex colours appear in any new CSS rules
- [ ] No new pip packages were installed
