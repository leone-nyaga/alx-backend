import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

// Product list
const listProducts = [
  {
    id: 1, name: 'Suitcase 250', price: 50, stock: 4,
  },
  {
    id: 2, name: 'Suitcase 450', price: 100, stock: 10,
  },
  {
    id: 3, name: 'Suitcase 650', price: 350, stock: 2,
  },
  {
    id: 4, name: 'Suitcase 1050', price: 550, stock: 5,
  },
];

// Redis client setup
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Function to get item by id
const getItemById = (id) => listProducts.find((item) => item.id === id);

// Function to reserve stock by id
const reserveStockById = async (itemId, stock) => {
  await setAsync(`item.${itemId}`, stock);
};

// Function to get current reserved stock by id
const getCurrentReservedStockById = async (itemId) => {
  const stock = await getAsync(`item.${itemId}`);
  return stock !== null ? parseInt(stock, 10) : null;
};

// Express app setup
const app = express();
const port = 1245;

// Route to get the list of products
app.get('/list_products', (req, res) => {
  res.json(listProducts.map((item) => ({
    itemId: item.id,
    itemName: item.name,
    price: item.price,
    initialAvailableQuantity: item.stock,
  })));
});

// Route to get product details by id
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);

  if (!item) {
    return res.json({ status: 'Product not found' });
  }

  const currentStock = await getCurrentReservedStockById(itemId) || item.stock;

  return res.json({
    itemId: item.id,
    itemName: item.name,
    price: item.price,
    initialAvailableQuantity: item.stock,
    currentQuantity: currentStock,
  });
});

// Route to reserve a product by id
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);

  if (!item) {
    return res.json({ status: 'Product not found' });
  }

  const currentStock = await getCurrentReservedStockById(itemId) || item.stock;

  if (currentStock <= 0) {
    return res.json({ status: 'Not enough stock available', itemId: item.id });
  }

  await reserveStockById(itemId, currentStock - 1);
  return res.json({ status: 'Reservation confirmed', itemId: item.id });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
