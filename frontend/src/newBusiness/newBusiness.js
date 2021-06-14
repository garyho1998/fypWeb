import React from "react";
import { useState } from "react";
import { getNewBusinessMatch } from "./newBusinessDao";
import LoadingBackdrop from "./loadingBackdrop";
import ResultedITList from "./resultedITList";
import SearchArea from "./searchArea";

export default function NewBusiness(props) {
  const [businessParagraph, setbusinessParagraph] = useState("");
  const [itSolutions, setitSolutions] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearchClick = (event) => {
    setLoading(true);
    getNewBusinessMatch(businessParagraph).then((res) => {
      // console.log("res", res);
      setitSolutions(res);
      // console.log("itSolutions", itSolutions);
      setLoading(false);
      props.setShowResult(true);
    });
  };

  return (
    <div>
      {props.showResult ? (
        <ResultedITList itSolutions={itSolutions}></ResultedITList>
      ) : (
        <SearchArea
          handleSearchClick={handleSearchClick}
          setbusinessParagraph={setbusinessParagraph}
          s></SearchArea>
      )}
      {loading && (
        <LoadingBackdrop showResult={props.setShowResult}></LoadingBackdrop>
      )}
    </div>
  );
}
