import frappe

def execute(filters=None):
    columns = [
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse"},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item"},
        {"label": "Projected Qty", "fieldname": "projected_qty", "fieldtype": "Float"},
        {"label": "Reserved Qty", "fieldname": "reserved_qty", "fieldtype": "Float"},
        {"label": "Reserved Qty for Production", "fieldname": "reserved_qty_for_production", "fieldtype": "Float"},
        {"label": "Reserved Qty for Sub Contract", "fieldname": "reserved_qty_for_sub_contract", "fieldtype": "Float"},
        {"label": "Actual Qty", "fieldname": "actual_qty", "fieldtype": "Float"},
        {"label": "Valuation Rate", "fieldname": "valuation_rate", "fieldtype": "Currency"}
    ]
    data = []
    sql_query = """
        SELECT
            bin.warehouse,
            bin.item_code,
            bin.projected_qty,
            bin.reserved_qty,
            bin.reserved_qty_for_production,
            bin.reserved_qty_for_sub_contract,
            bin.actual_qty,
            bin.valuation_rate
        FROM
            `tabBin` bin
        WHERE
            (bin.projected_qty != 0 OR 
            bin.reserved_qty != 0 OR 
            bin.reserved_qty_for_production != 0 OR 
            bin.reserved_qty_for_sub_contract != 0 OR 
            bin.actual_qty != 0)
        ORDER BY
            bin.warehouse,
            bin.item_code
    """
    
    index_queries = [
        "CREATE INDEX IF NOT EXISTS idx_warehouse_item_code ON `tabBin` (warehouse, item_code)",
        "CREATE INDEX IF NOT EXISTS idx_projected_qty ON `tabBin` (projected_qty)",
        "CREATE INDEX IF NOT EXISTS idx_reserved_qty ON `tabBin` (reserved_qty)",
        "CREATE INDEX IF NOT EXISTS idx_reserved_qty_for_production ON `tabBin` (reserved_qty_for_production)",
        "CREATE INDEX IF NOT EXISTS idx_reserved_qty_for_sub_contract ON `tabBin` (reserved_qty_for_sub_contract)",
        "CREATE INDEX IF NOT EXISTS idx_actual_qty ON `tabBin` (actual_qty)"
    ]
    
    for query in index_queries:
        try:
            frappe.db.sql(query)
        except Exception as e:
            print(f"Error creating index: {e}")

    stock_entries = frappe.db.sql(sql_query, as_dict=True)

    for row in stock_entries:
        data.append(row)

    return columns, data

