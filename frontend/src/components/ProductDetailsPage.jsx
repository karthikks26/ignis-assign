import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

const ProductDetailsPage = () => {
  const { url } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/products/");
        const decodedUrl = decodeURIComponent(url);
        const foundProduct = response.data.find(
          (product) => product.url === decodedUrl
        );
        if (foundProduct) {
          setProduct(foundProduct);
        } else {
          setError("Product not found.");
        }
      } catch (err) {
        setError("Error fetching product data.");
        console.error("Error fetching product data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [url]);

  // Function to clean and format the description
  const formatDescription = (description) => {
    return description
      .replace(/â€¢/g, "•") // Replace special bullet character
      .replace(/â/g, " ") // Remove unwanted characters
      .replace(/\n/g, "<br />") // Replace newlines with HTML line breaks
      .split("<br />") // Split the description by line breaks
      .map((line, index) => <p key={index}>{line}</p>); // Map each line to a paragraph
  };

  if (loading)
    return (
      <p className="text-center text-gray-500">Loading product details...</p>
    );
  if (error) return <p className="text-center text-red-500">{error}</p>;

  return (
    <div className="bg-gray-50 min-h-screen py-8 px-4">
      {product && (
        <div className="max-w-4xl mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
          <img
            src={product.image_url}
            alt={product.title}
            className="w-full h-80 object-cover"
          />
          <div className="p-6">
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              {product.title}
            </h1>
            <p className="text-xl text-gray-600 mb-2">
              Price: ₹{product.price}
            </p>
            <p className="text-xl text-gray-600 mb-4">MRP: ₹{product.mrp}</p>
            <div className="text-lg text-gray-700 mb-4">
              {formatDescription(product.description)}
            </div>
            <p className="text-lg text-gray-700 mb-4">
              Sale: {product.last_7_day_sale}
            </p>

            {/* Display color and size options */}
            {product.available_skus.length > 0 && (
              <div className="mt-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-2">
                  Available Options:
                </h2>
                {product.available_skus.map((sku, index) => (
                  <div key={index} className="mb-4">
                    <p className="text-lg font-semibold text-gray-800">
                      Color: {sku.color}
                    </p>
                    <p className="text-lg font-semibold text-gray-800">
                      Sizes:
                    </p>
                    <ul className="list-disc pl-6 text-gray-700">
                      {sku.size.map((size, idx) => (
                        <li key={idx} className="text-lg">
                          {size}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductDetailsPage;
