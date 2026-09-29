cube(`Products`, {
  sql: `SELECT * FROM products_gold`,
  title: `Products`,
  description: `One row per product.`,

  measures: {
    productCount: {
      type: `count`,
      description: `Count of products.`
    }
  },

  dimensions: {
    productId: {
      sql: `product_id`,
      type: `string`,
      primaryKey: true
    },
    productName: {
      sql: `product_name`,
      type: `string`
    },
    category: {
      sql: `category`,
      type: `string`
    },
    subcategory: {
      sql: `subcategory`,
      type: `string`
    },
    listPrice: {
      sql: `list_price`,
      type: `number`
    },
    productStatus: {
      sql: `product_status`,
      type: `string`
    }
  }
});
