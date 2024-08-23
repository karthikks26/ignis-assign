import React from "react";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const navigate = useNavigate();

  const handleImageClick = (imageUrl) => {
    navigate(`/products?imageUrl=${encodeURIComponent(imageUrl)}`);
  };

  return (
    <div className="bg-gray-50 min-h-screen py-8">
      <h1 className="text-4xl font-semibold text-center text-gray-800 mb-6">
        Yoo Store
      </h1>
      <div className="grid grid-cols-3 gap-6 max-w-4xl mx-auto">
        {[
          "https://nobero.com/cdn/shop/files/t-shirts_68004d61-294b-4156-967b-0a5a8638d3f1.jpg?v=1719231626",
          "https://nobero.com/cdn/shop/files/2_4.png?v=1719231678",
          "https://nobero.com/cdn/shop/files/8_22a87a7c-82fa-446e-93e1-af1f0f742eef.png?v=1697452265",
          "https://nobero.com/cdn/shop/files/9_74d1b95d-04db-4358-8406-05a744e0fd65.png?v=1697452265",
          "https://nobero.com/cdn/shop/files/10_ba94e30c-4d53-4814-9c8a-5bc14d131d6b.png?v=1697452265",
          "https://nobero.com/cdn/shop/files/SHOP_WOMEN_MEN_MOBILE_Vers._1.jpg?v=1716790197",
        ].map((src, index) => (
          <div key={index} className="w-full max-w-xs mx-auto">
            <img
              src={src}
              alt={`image-${index + 1}`}
              className="w-full h-auto rounded-lg shadow-sm transform transition-transform duration-300 hover:scale-105 cursor-pointer"
              onClick={() => handleImageClick(src)}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePage;
