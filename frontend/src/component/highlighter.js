import "./component.css";
export default function Highlighter(props) {
  if (!props.answer) return <div>{props.text}</div>;
  var result = props.text.replace(
    props.answer.toString(),
    "<span class='highlighter'>" + props.answer + "</span>"
  );
  return <div dangerouslySetInnerHTML={{ __html: result }} />;
}
