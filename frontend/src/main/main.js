import { useState, useEffect } from "react";
import { CartContainer } from "../shopping-cart/components/cartContainer";
import { Link } from "react-router-dom";
import "./main.css";
import NewBusiness from "../newBusiness/newBusiness";

import MatchDataPage from "../businessList/matchDataPage";
import Divider from "@material-ui/core/Divider";

export const Main = ({ page, notFound }) => {
  const [pageState, setPageState] = useState(page);
  const [showResult, setShowResult] = useState(false);
  const handleCartIcon = () => {
    setPageState("cart");
  };

  const handleBusinessListIcon = () => {
    setPageState("businessList");
  };

  const handleHomeIcon = () => {
    setPageState("home");
    setShowResult(false);
  };

  const pageRenderSwitch = (pageState) => {
    switch (pageState) {
      case "businessList":
        return <MatchDataPage></MatchDataPage>;
      default:
        return (
          <NewBusiness showResult={showResult} setShowResult={setShowResult} />
        );
    }
  };

  return (
    <div className="main">
      <div>
        <header className="header">
          <Link className="header-child" to="/" onClick={handleHomeIcon}>
            Home
          </Link>
          <Link
            className="header-child"
            to="/businessList"
            onClick={handleBusinessListIcon}>
            Business Needs
          </Link>
          <Link className="header-child">IT Solutions</Link>
          <Link className="header-child">Contact Us</Link>
          <Link className="header-child">Documents</Link>
        </header>
        <Divider />
        {/* <div className="text-center mt-4">
          <h4>HKU FYP Business Matching</h4>
          <p className="mt-3" style={{ color: "#aaaaaa" }}>
            This is a business matching web app powered by Deep learning
          </p>
        </div> */}
      </div>
      <div>
        {notFound ? (
          <div className="mt-5 text-center">
            Seems you are lost, go back to <Link to="/">home</Link>
          </div>
        ) : (
          pageRenderSwitch(pageState)
        )}
      </div>
    </div>
  );
};
