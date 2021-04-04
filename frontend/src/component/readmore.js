import "./component.css";
import { useState, useEffect } from "react";

export default function Highlighter(props) {
  const [paragraph, setDescription] = useState(props.paragraph);
  const [paragraphExtra, setDescriptionExtra] = useState("");
  const [readMore, setReadMore] = useState(false);
  const linkName = readMore ? "Read Less" : "Read More";
  const maxLength = 150;
  useEffect(() => {
    if (props.paragraph.length > maxLength) {
      setDescription(props.paragraph.slice(0, maxLength));
      setDescriptionExtra(props.paragraph.slice(maxLength));
    }
  }, [props.paragraph]);

  return (
    <div>
      {" "}
      {paragraph}
      {readMore && paragraphExtra}
      <div
        className="read-more-link"
        onClick={() => {
          setReadMore(!readMore);
        }}>
        {linkName}
      </div>
    </div>
  );
}
