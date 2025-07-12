import { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const flaskUrl = window.__ENV__.API_URL;
  const flaskPort = window.__ENV__.API_PORT;
  const [products, setProducts] = useState([]);
  const [lowStock, setLowStock] = useState([]);
  const [restocks, setRestocks] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [newProduct, setNewProduct] = useState({
  name: '',
  description: '',
  sku: '',
  category: '',
  price: '',
  quantity: '',
  threshold: ''
  });


  console.log(import.meta.env);

  useEffect(() => {
    fetchProducts();
    fetchLowStock();
    fetchRestocks();
  }, []);

  const fetchProducts = async () => {
    const res = await axios.get(`http://${flaskUrl}:${flaskPort}/api/products`);
    setProducts(res.data);
  };

  const fetchLowStock = async () => {
    const res = await axios.get(`http://${flaskUrl}:${flaskPort}/api/products/low-stock`);
    setLowStock(res.data);
  };

  const fetchRestocks = async () => {
    const res = await axios.get(`http://${flaskUrl}:${flaskPort}/api/restocks`);
    setRestocks(res.data);
  };

  const handleSelect = async (id) => {
    const res = await axios.get(`http://${flaskUrl}:${flaskPort}/api/products/${id}`);
    setSelectedProduct(res.data);
  };

  const handleAddStock = async (id) => {
    const quantity = prompt("Enter quantity to add:");
    if (!quantity) return;

    await axios.put(`http://${flaskUrl}:${flaskPort}/api/products/${id}`, {
      quantity_to_add: parseInt(quantity)
    });

    fetchProducts();
    fetchRestocks();
    fetchLowStock();
  };

  return (
    <div className="App">
      <h1>Inventory Dashboard</h1>

      <section>
        <h2>Add New Product</h2>
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            try {
              await axios.post(`http://${flaskUrl}:${flaskPort}/api/products`, {
                ...newProduct,
                price: parseFloat(newProduct.price),
                quantity: parseInt(newProduct.quantity),
                threshold: parseInt(newProduct.threshold)
              });
              setNewProduct({
                name: '',
                description: '',
                sku: '',
                category: '',
                price: '',
                quantity: '',
                threshold: ''
              });
              fetchProducts();
              fetchLowStock();
              fetchRestocks();
            } catch (err) {
              alert('Failed to add product: ' + err.response?.data?.error || err.message);
            }
          }}
        >
          <input
            type="text"
            placeholder="Name"
            value={newProduct.name}
            onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Description"
            value={newProduct.description}
            onChange={(e) => setNewProduct({ ...newProduct, description: e.target.value })}
          />
          <input
            type="text"
            placeholder="SKU"
            value={newProduct.sku}
            onChange={(e) => setNewProduct({ ...newProduct, sku: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Category"
            value={newProduct.category}
            onChange={(e) => setNewProduct({ ...newProduct, category: e.target.value })}
          />
          <input
            type="number"
            placeholder="Price"
            value={newProduct.price}
            onChange={(e) => setNewProduct({ ...newProduct, price: e.target.value })}
            required
          />
          <input
            type="number"
            placeholder="Initial Quantity"
            value={newProduct.quantity}
            onChange={(e) => setNewProduct({ ...newProduct, quantity: e.target.value })}
          />
          <input
            type="number"
            placeholder="Threshold"
            value={newProduct.threshold}
            onChange={(e) => setNewProduct({ ...newProduct, threshold: e.target.value })}
          />
          <button type="submit">Add Product</button>
        </form>
      </section>


      <section>
        <h2>All Products</h2>
        <ul>
          {products.map((p) => (
            <li key={p.id}>
              {p.name} - Qty: {p.quantity}
              <button onClick={() => handleSelect(p.id)}>View</button>
              <button onClick={() => handleAddStock(p.id)}>Restock</button>
            </li>
          ))}
        </ul>
      </section>

      {selectedProduct && (
        <section>
          <h2>Selected Product</h2>
          <p><strong>ID:</strong> {selectedProduct.id}</p>
          <p><strong>Name:</strong> {selectedProduct.name}</p>
          <p><strong>SKU:</strong> {selectedProduct.sku}</p>
          <p><strong>Price:</strong> ${selectedProduct.price}</p>
          <p><strong>Quantity:</strong> {selectedProduct.quantity}</p>
        </section>
      )}

      <section>
        <h2>Low Stock Alerts</h2>
        {lowStock.length === 0 ? (
          <p>No low stock products</p>
        ) : (
          <ul>
            {lowStock.map((item) => (
              <li key={item.product_id}>
                {item.product_name} - Qty: {item.quantity}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section>
        <h2>Restock History</h2>
        <ul>
          {restocks.map((r) => (
            <li key={r.restock_id}>
              Product {r.product_id}: +{r.quantity_added} on {new Date(r.restock_date).toLocaleString()} — {r.notes}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export default App;

