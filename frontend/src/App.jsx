import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./components/HomePage.jsx";
import ProductsPage from "./components/ProductPage.jsx";
import ProductDetailsPage from "./components/ProductDetailsPage.jsx"; // Import the ProductDetailsPage component

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/product/:url" element={<ProductDetailsPage />} />{" "}
        {/* Route for product details */}
      </Routes>
    </Router>
  );
};

export default App;
