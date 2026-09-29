cube(`Inventory`, {
  sql: `SELECT * FROM inventory_gold`,
  title: `Inventory`,
  description: `Product-day inventory snapshots. Inventory facts must be aggregated independently from order-line sales facts.`,

  measures: {
    inventoryOnHand: {
      sql: `inventory_on_hand`,
      type: `sum`,
      description: `Inventory units on hand at product-day snapshot grain.`
    },
    lowStockRows: {
      type: `count`,
      filters: [{ sql: `${CUBE}.low_stock_flag = TRUE` }],
      description: `Count of product-day snapshots at or below reorder point.`
    },
    salesVelocityUnitsPerDay: {
      sql: `sales_velocity_units_per_day`,
      type: `avg`,
      description: `Average completed-order units per day over the 30 calendar days before each snapshot.`
    },
    stockCoverageDays: {
      sql: `stock_coverage_days`,
      type: `avg`,
      description: `Average product-day stock coverage; use coverage status to distinguish no-demand values.`
    }
  },

  dimensions: {
    snapshotProductKey: {
      sql: `${CUBE}.product_id || '_' || CAST(${CUBE}.snapshot_date AS VARCHAR)`,
      type: `string`,
      primaryKey: true,
      public: false
    },
    snapshotDate: {
      sql: `snapshot_date`,
      type: `time`
    },
    productId: {
      sql: `product_id`,
      type: `string`
    },
    reorderPoint: {
      sql: `reorder_point`,
      type: `number`
    },
    lowStockFlag: {
      sql: `low_stock_flag`,
      type: `boolean`
    },
    stockCoverageStatus: {
      sql: `stock_coverage_status`,
      type: `string`
    }
  },

  joins: {
    Products: {
      relationship: `belongsTo`,
      sql: `${CUBE}.product_id = ${Products}.product_id`
    }
  }
});
