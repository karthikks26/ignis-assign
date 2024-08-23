import React, { useEffect, useState } from "react";
import axios from "axios";
import { useLocation, Link } from "react-router-dom";

const ProductsPage = () => {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const imageUrl = queryParams.get("imageUrl");

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/products/");
        setProducts(response.data);
      } catch (err) {
        setError("Error fetching products data.");
        console.error("Error fetching products data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  useEffect(() => {
    if (products.length > 0 && imageUrl) {
      const filtered = products.filter(
        (product) => product.category_image_url === imageUrl
      );
      setFilteredProducts(filtered);
    }
  }, [products, imageUrl]);
  console.log(products);

  if (loading)
    return <p className="text-center text-gray-500">Loading products...</p>;
  if (error) return <p className="text-center text-red-500">{error}</p>;

  return (
    <div className="bg-gray-50 min-h-screen py-8 px-4">
      <h1 className="text-3xl font-semibold text-center text-gray-800 mb-6">
        Products
      </h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {filteredProducts.length > 0 ? (
          filteredProducts.map((product) => (
            <div
              key={product.url}
              className="bg-white border rounded-lg shadow-sm p-4 flex flex-col items-center"
            >
              <img
                src={product.image_url}
                alt={product.title}
                className="w-full h-48 object-cover rounded-md mb-2"
              />
              <h2 className="text-lg font-semibold text-gray-800 mb-1">
                {product.title}
              </h2>
              <p className="text-md text-gray-600 mb-2">₹{product.price}</p>
              <Link
                to={`/product/${encodeURIComponent(product.url)}`}
                className="text-blue-600 hover:underline"
              >
                View Details
              </Link>
            </div>
          ))
        ) : (
          <p className="text-center text-gray-600">
            No products found for this image.
          </p>
        )}
      </div>
    </div>
  );
};

export default ProductsPage;
