# TODO

## Engineering Improvements (POS)

- [x] Remove insecure hardcoded default admin password insertion (admin123) and add safe first-run behavior.

- [x] Replace calculator `eval()` usage with a safe expression evaluator.

- [ ] Make checkout DB operations atomic using a single SQLite transaction; prevent overselling.

- [ ] Add useful SQLite indexes for performance (products name/barcode, sales date, sale_items sale_id/product_id).
- [ ] Fix receipt generation to avoid brittle tuple indexing (use explicit column SELECT or dict mapping).
- [ ] Remove/merge duplicated `InventoryManager` implementations (`inventory_manager.py` vs `inventorymanagement.py`).
- [ ] Smoke test: login, add to cart, checkout, generate receipt, run reports.

